import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import google.generativeai as genai
import time
import os
from dotenv import load_dotenv
import requests # Import the requests library
import json # Import the json library

# Load environment variables from a .env file
load_dotenv()

# --- Configuration ---
# The API key is now loaded from the .env file (e.g., GEMINI_API_KEY="...")
API_KEY = os.getenv("GEMINI_API_KEY")

# --- Page Setup ---
st.set_page_config(
    page_title="Anarix AI - AI Sales Analyst",
    page_icon="🤖",
    layout="wide",
)

# --- Database Schema ---
DB_SCHEMA = """
CREATE TABLE product_ad_sales (
    date DATETIME,
    item_id INTEGER,
    ad_sales FLOAT,
    impressions INTEGER,
    ad_spend FLOAT,
    clicks INTEGER,
    units_sold INTEGER
);

CREATE TABLE total_sales (
    date DATETIME,
    item_id INTEGER,
    total_sales FLOAT,
    total_units_ordered INTEGER
);

CREATE TABLE eligibility_table (
    eligibility_datetime_utc DATETIME,
    item_id INTEGER,
    eligibility TEXT,
    message TEXT
);
"""

# --- Gemini LLM Configuration ---
def configure_llm(api_key):
    """Configures the Generative AI model with the provided API key."""
    try:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-2.0-flash')
    except Exception as e:
        st.error(f"Failed to configure Gemini API: {e}")
        return None

# --- Core Functions ---

def get_sql_from_llm(model, question):
    """
    Uses the LLM to convert a natural language question into an SQL query.
    This version now builds and shows the raw HTTP request.
    """
    prompt = f"""
    Given the following database schema:
    {DB_SCHEMA}

    Your task is to convert the following user question into a syntactically correct SQLite query.
    You must only output the SQL query itself. Do not include any other text, markdown formatting, or explanations.
    Your response should start directly with the SQL command (e.g., SELECT ...).
    
    IMPORTANT INSTRUCTIONS:
    - Do not add any text or characters like 'ite' before the `SELECT` statement.
    - If the user asks for a "total" of a column (like 'what are the total sales'), you MUST use the SUM() aggregation function. For example: `SELECT SUM(total_sales) FROM total_sales`.
    - If the user asks for "top 5", "highest 5", or similar, you should use `ORDER BY ... DESC LIMIT 5`.
    - If the user asks for CPC (Cost Per Click), the formula is `ad_spend / clicks`. You must handle cases where clicks might be zero to avoid division by zero errors. For example: `WHERE clicks > 0`.

    Question: "{question}"

    SQL Query:
    """
    
    # --- Manually build the API request ---
    api_endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }

    # --- Print the raw request details to the terminal ---
    print("--- RAW API REQUEST ---")
    print(f"Endpoint: {api_endpoint}")
    print(f"Headers: {json.dumps(headers, indent=2)}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    print("-----------------------")

    try:
        # Make the POST request
        response = requests.post(api_endpoint, headers=headers, json=payload)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        
        # Extract the text from the response JSON
        response_data = response.json()
        raw_text = response_data['candidates'][0]['content']['parts'][0]['text']
        
        # --- MORE ROBUST PARSING ---
        # Find the start of the SQL query (e.g., 'SELECT') and trim any leading text.
        select_pos = raw_text.upper().find('SELECT')
        if select_pos != -1:
            sql_query = raw_text[select_pos:]
        else:
            # Fallback for other potential SQL commands, or just clean the raw text
            sql_query = raw_text

        # Final cleanup of any remaining markdown code blocks
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
        # --- END OF ROBUST PARSING ---
        
        return sql_query
        
    except requests.exceptions.RequestException as e:
        st.error(f"Error making API request: {e}")
        return None
    except (KeyError, IndexError) as e:
        st.error(f"Error parsing API response: {e}")
        print(f"Full response data: {response.json()}")
        return None


def execute_sql_query(query, db_path="sales.db"):
    """
    Executes an SQL query on the SQLite database and returns the result as a DataFrame.
    """
    if not os.path.exists(db_path):
        st.error(f"Database file not found at '{db_path}'. Please ensure the database exists.")
        return None
    try:
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql_query(query, conn)
        return df
    except sqlite3.Error as e:
        st.error(f"Database Error: {e}")
        st.warning(f"Failed Query: `{query}`")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred while querying the database: {e}")
        return None


def get_human_response_from_llm(model, question, data):
    """
    Generates a human-readable response based on the query result.
    (This function still uses the SDK for simplicity, but the principle is the same)
    """
    prompt = f"""
    You are a helpful AI assistant specializing in analyzing sales and advertising data.
    A user asked the following question: "{question}"
    The following data was retrieved from the database to answer the question:
    {data.to_string()}
    Based on this data, provide a concise, easy-to-understand answer to the user's question.
    Analyze the data and provide a summary or key insights.
    Do not mention the database or SQL. Speak directly to the user.
    """
    try:
        response_stream = model.generate_content(prompt, stream=True)
        for chunk in response_stream:
            yield chunk.text
    except Exception as e:
        yield f"Error generating response: {e}"


def create_visualization(df, question):
    """
    Attempts to create a suitable Plotly visualization from the DataFrame,
    taking the user's original question into account.
    """
    if df is None or df.empty or len(df.columns) < 2:
        return None

    # Common theme for all charts
    template = "plotly_dark"

    date_cols = [col for col in df.columns if 'date' in col.lower()]
    if date_cols:
        try:
            df[date_cols[0]] = pd.to_datetime(df[date_cols[0]])
        except Exception:
            pass

    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    string_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

    # --- UPDATED LOGIC FOR PIE CHARTS ---
    if 'pie' in question.lower() and 'item_id' in df.columns:
        y_values = [col for col in numeric_cols if col.lower() != 'item_id']
        if y_values:
            try:
                df['item_id'] = df['item_id'].astype(str)
                fig = px.pie(df, names='item_id', values=y_values[0], title=f"Distribution of {y_values[0]} by Product", template=template)
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
                return fig
            except Exception:
                pass
    # --- END OF PIE CHART LOGIC ---

    # Bar chart for item_id aggregation
    if 'item_id' in df.columns and len(numeric_cols) >= 1:
        y_values = [col for col in numeric_cols if col.lower() != 'item_id']
        if not y_values:
            return None
        try:
            df['item_id'] = df['item_id'].astype(str)
            fig = px.bar(df, x='item_id', y=y_values[0], title=f"{y_values[0]} by Product (item_id)", template=template)
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
            return fig
        except Exception:
            return None

    if not numeric_cols:
        return None

    # Time series line chart
    if date_cols and len(numeric_cols) >= 1:
        try:
            fig = px.line(df, x=date_cols[0], y=numeric_cols, title="Time Series Analysis", markers=True, template=template)
            fig.update_layout(legend_title_text='Metrics', paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
            return fig
        except Exception:
            return None

    # Bar chart for general categorical data
    if string_cols and len(numeric_cols) >= 1:
        try:
            fig = px.bar(df, x=string_cols[0], y=numeric_cols[0], title=f"{numeric_cols[0]} by {string_cols[0]}", template=template)
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
            return fig
        except Exception:
            return None

    return None

def apply_custom_css():
    """Applies custom CSS to decorate the Streamlit UI."""
    st.markdown("""
    <style>
    /* Main app background */
    [data-testid="stAppViewContainer"] > .main {
        background: #000000;
        color: white;
    }

    /* Title styling */
    h1 {
        color: #FFFFFF;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Chat message styling */
    [data-testid="stChatMessage"] {
        background-color: #1E1E1E;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        margin-bottom: 1rem;
        border: 1px solid #333333;
    }

    /* Expander styling */
    [data-testid="stExpander"] {
        background-color: #1E1E1E;
        border-radius: 0.5rem;
        border: 1px solid #333333;
    }
    [data-testid="stExpander"] summary {
        font-weight: bold;
        color: #FFFFFF;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] > div:first-child {
        background: #000000;
        border-right: 1px solid #333333;
    }
    
    /* Style the chat input box */
    [data-testid="stChatInput"] {
        background-color: #1E1E1E;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Streamlit App UI ---

apply_custom_css()

st.sidebar.title("About")
st.sidebar.info(
    "This is an AI-powered chatbot that can answer questions about your sales data. "
    "It converts your questions into SQL queries, fetches the data, and visualizes the results."
)
st.sidebar.success("Powered by Google Gemini")


st.title("📈 Anarix.ai - An AI Agent to Answer E-commerce Data Questions")
st.markdown(
    '<p style="text-align: center; font-size:20px; color:gray;">Got questions about your product sales, ads, or eligibility? Just ask!</p>',
    unsafe_allow_html=True
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "model" not in st.session_state:
    st.session_state.model = None

# Configure the model if the API key is available
if API_KEY and not st.session_state.model:
    st.session_state.model = configure_llm(API_KEY)


# Display chat messages from history on app rerun
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sql" in message and message["sql"]:
            with st.expander("Generated SQL Query"):
                st.code(message["sql"], language="sql")
        if "df" in message and message["df"] is not None and not message["df"].empty:
            st.dataframe(message["df"])
        if "fig" in message and message["fig"] is not None:
            # Add a unique key to each chart in the history
            st.plotly_chart(message["fig"], use_container_width=True, key=f"history_chart_{i}")


# Main chat interface
if prompt := st.chat_input("Ask a question about your sales data..."):
    if not st.session_state.model:
        st.error("API Key not configured. Please ensure your .env file is set up correctly.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        sql_query = ""
        df = None
        fig = None

        with st.spinner("Thinking..."):
            sql_query = get_sql_from_llm(st.session_state.model, prompt)

            if sql_query:
                df = execute_sql_query(sql_query)

                if df is not None:
                    if not df.empty:
                        response_generator = get_human_response_from_llm(st.session_state.model, prompt, df)
                        for chunk in response_generator:
                            full_response += chunk
                            message_placeholder.markdown(full_response + "▌")
                            time.sleep(0.01)
                        message_placeholder.markdown(full_response)
                        # Pass the original prompt to the visualization function
                        fig = create_visualization(df, prompt)
                    else:
                        full_response = "I found no data for your query. Please try asking something else."
                        message_placeholder.markdown(full_response)
                else:
                    full_response = "I couldn't retrieve the data. Please check the error messages above."
                    message_placeholder.markdown(full_response)
            else:
                full_response = "I'm sorry, I had trouble understanding that. Could you please rephrase your question?"
                message_placeholder.markdown(full_response)

        # Display results below the streamed response
        if sql_query:
            with st.expander("Generated SQL Query"):
                st.code(sql_query, language="sql")
        if df is not None and not df.empty:
            st.dataframe(df)
        if fig is not None:
            # Add a unique key to the newly generated chart
            st.plotly_chart(fig, use_container_width=True, key=f"current_chart_{len(st.session_state.messages)}")

    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response,
        "sql": sql_query,
        "df": df,
        "fig": fig
    })

**AI-Powered Sales Data Chatbot**
This project is a sophisticated AI-powered chatbot built with Streamlit that allows users to conversationally query a sales and advertising database. Users can ask questions in plain English, and the application will translate them into SQL queries, fetch the data, and present the results in a human-readable format, complete with dynamic visualizations.

**Key Features Natural Language to SQL: **
Leverages Google's Gemini 2.0 Flash model to understand user questions and convert them into precise SQLite queries. _Dynamic Visualizations: _Automatically generates interactive bar charts, pie charts, and time-series graphs based on the query results, providing instant visual insights. Raw API Request Logging: For technical demonstrations, the application can print the raw JSON payload and headers of the API call to the terminal. Streaming Responses: Simulates a real-time conversation by streaming the AI's text-based answers. Customizable UI: Features a sleek, modern user interface with a dark theme, which can be easily customized using CSS within the Streamlit application. Error Handling: Includes robust error handling for database connection issues, invalid SQL queries, and API call failures.

**Tech Stack **
Frontend: Streamlit 
Backend: Python
Database: SQLite
AI Model: Google Gemini 2.0 Flash
Data Manipulation: Pandas 
Visualizations: Plotly Express 
API Requests: requests library

**How It Works User Input:** The user asks a question in the chat interface (e.g., "What were the top 5 products by total sales?").
**NL to SQL:** The application sends the question, along with the database schema and specific instructions, to the Gemini API.
**SQL Generation:** The Gemini model returns a syntactically correct SQLite query.
**Database Query:** The application executes this query against the local sales.db database.
**Data Analysis & Visualization:** The retrieved data is analyzed to generate a human-readable summary and a relevant Plotly visualization.
**Display Results:** The summary, the generated SQL query (in an expander), the raw data (in a DataFrame), and the visualization are all displayed in the chat interface.

**Install dependencies:**
pip install -r requirements.txt
**
Set up the database:**
Place your SQLite database file named sales.db in the root directory of the project.

**Configure environment variables:**
Create a file named .env in the root directory. Add your Google Gemini API key to the .env file: GEMINI_API_KEY="YOUR_API_KEY_HERE"

**Run the application:**
streamlit run app.py

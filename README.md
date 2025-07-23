**AI-Powered Sales Data Chatbot**
This project is a sophisticated AI-powered chatbot built with Streamlit that allows users to conversationally query a sales and advertising database. Users can ask questions in plain English, and the application will translate them into SQL queries, fetch the data, and present the results in a human-readable format, complete with dynamic visualizations.

**Key Features Natural Language to SQL:**
Leverages Google's Gemini 2.0 Flash model to understand user questions and convert them into precise SQLite queries. _Dynamic Visualizations: _Automatically generates interactive bar charts, pie charts, and time-series graphs based on the query results, providing instant visual insights. Raw API Request Logging: For technical demonstrations, the application can print the raw JSON payload and headers of the API call to the terminal. Streaming Responses: Simulates a real-time conversation by streaming the AI's text-based answers. Customizable UI: Features a sleek, modern user interface with a dark theme, which can be easily customized using CSS within the Streamlit application. Error Handling: Includes robust error handling for database connection issues, invalid SQL queries, and API call failures.

| Category         | Technology               |
|------------------|---------------------------|
| **Frontend**     | Streamlit                |
| **Backend**      | Python                   |
| **Database**     | SQLite                   |
| **AI Model**     | Google Gemini 2.0 Flash  |
| **Data Handling**| Pandas                   |
| **Visualizations**| Plotly Express          |
| **API Requests** | `requests` library       |


**How It Works User Input:** The user asks a question in the chat interface (e.g., "What were the top 5 products by total sales?").
**NL to SQL:** The application sends the question, along with the database schema and specific instructions, to the Gemini API.
**SQL Generation:** The Gemini model returns a syntactically correct SQLite query.
**Database Query:** The application executes this query against the local sales.db database.
**Data Analysis & Visualization:** The retrieved data is analyzed to generate a human-readable summary and a relevant Plotly visualization.
**Display Results:** The summary, the generated SQL query (in an expander), the raw data (in a DataFrame), and the visualization are all displayed in the chat interface.

**Install dependencies:**
pip install -r requirements.txt

**Set up the database:**
Place your SQLite database file named sales.db in the root directory of the project.

**Configure environment variables:**
Create a file named .env in the root directory. Add your Google Gemini API key to the .env file: GEMINI_API_KEY="YOUR_API_KEY_HERE"

**Run the application:**
streamlit run app.py


<img width="1919" height="822" alt="image" src="https://github.com/user-attachments/assets/d1d2771e-cf24-4fd6-a94d-e79fba5a91ca" />

<img width="1919" height="833" alt="image" src="https://github.com/user-attachments/assets/7afde840-790b-4457-baeb-690f5bb6779f" />

<img width="1919" height="835" alt="image" src="https://github.com/user-attachments/assets/dfa4d40b-d51d-46e3-9d9d-d273540e19ae" />

<img width="1879" height="765" alt="image" src="https://github.com/user-attachments/assets/9cbb0787-8320-45a7-a544-31d75493daa8" />
<img width="1909" height="834" alt="image" src="https://github.com/user-attachments/assets/293f6388-5212-4a78-accc-881d7ad2454e" />

<img width="1918" height="814" alt="image" src="https://github.com/user-attachments/assets/c5f94912-a8a3-4fa4-9ed4-e3c8cf5a60c5" />
<img width="1919" height="819" alt="image" src="https://github.com/user-attachments/assets/8640671e-e53d-43db-b52b-c3b57cd8c1f5" />

<img width="1919" height="823" alt="image" src="https://github.com/user-attachments/assets/99105552-deff-4878-b11d-35e2dba9c641" />
<img width="1917" height="817" alt="image" src="https://github.com/user-attachments/assets/91ce15c1-fc56-4d3c-8b91-4f9b1ac68a23" />


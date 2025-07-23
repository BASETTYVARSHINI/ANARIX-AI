# 🧠 AI-Powered Sales Data Chatbot

This project is a sophisticated AI-powered chatbot built with **Streamlit** that allows users to **conversationally query a sales and advertising database**.

Users can ask questions in plain English, and the app converts them into SQL queries, fetches the data from SQLite, and presents the results with dynamic visualizations — all in real-time.

---

## 🚀 Key Features

- **🧾 Natural Language to SQL**: Leverages **Google Gemini 2.0 Flash** to convert user questions into precise SQLite queries.
- **📊 Dynamic Visualizations**: Auto-generates interactive bar charts, pie charts, and time-series graphs using **Plotly Express**.
- **🔍 Raw API Request Logging**: Prints the raw JSON payload and headers for debugging and technical demos.
- **💬 Streaming Responses**: Simulates real-time AI conversations with streamed responses.
- **🎨 Customizable UI**: Features a modern **dark theme**; customizable with CSS inside the Streamlit app.
- **🛡️ Robust Error Handling**: Manages issues like DB connection errors, invalid SQL, and API failures gracefully.

---

## 🛠️ Tech Stack

| Category          | Technology               |
|------------------|---------------------------|
| **Frontend**     | Streamlit                |
| **Backend**      | Python                   |
| **Database**     | SQLite                   |
| **AI Model**     | Google Gemini 2.0 Flash  |
| **Data Handling**| Pandas                   |
| **Visualizations**| Plotly Express          |
| **API Requests** | `requests` library       |

---

## ⚙️ How It Works

1. **User Input**  
   The user types a natural language question (e.g., _"What were the top 5 products by total sales?"_).

2. **Natural Language to SQL**  
   The app sends the question, along with the DB schema and prompt instructions, to the Gemini API.

3. **SQL Query Generation**  
   Gemini returns a valid, syntactically correct SQLite query.

4. **Database Query Execution**  
   The query is executed on the local `sales.db` file.

5. **Data Analysis & Visualization**  
   The resulting data is summarized and visualized with **Plotly Express**.

6. **Display Results**  
   - ✅ Natural Language Answer  
   - 🧮 SQL Query (in an expander)  
   - 🧾 Raw DataFrame Output  
   - 📊 Visual Graph (Bar, Line, Pie, etc.)

---

## 🔧 Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
2. Set Up the Database
Place your SQLite database file in the project root and name it:

Copy
Edit
sales.db
3. Configure Environment Variables
Create a .env file in the root directory and add your Gemini API key:

ini
Copy
Edit
GEMINI_API_KEY="YOUR_API_KEY_HERE"
4. Run the Application
bash
Copy
Edit
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


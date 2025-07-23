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
sales.db

3. Configure Environment Variables
Create a .env file in the root directory and add your Gemini API key:
ini
GEMINI_API_KEY="YOUR_API_KEY_HERE"

4. Run the Application
streamlit run app.py


## 📸 Screenshots

### 🔍 Chat Interface and Results
<img width="1919" height="833" alt="image" src="https://github.com/user-attachments/assets/a6f57a28-aeb8-49ad-9a0a-58a00462b457" />

<img width="1919" height="832" alt="image" src="https://github.com/user-attachments/assets/b9038a27-a587-45db-a9fd-ff2d89b087c3" />

<img width="1919" height="826" alt="image" src="https://github.com/user-attachments/assets/f1082449-1f7d-48ab-bf92-b20005bfcf9b" />

<img width="1919" height="834" alt="image" src="https://github.com/user-attachments/assets/7613f132-3a74-42ad-b1d6-68172726ecf3" />


### 📊 Visualizations

<img width="1919" height="832" alt="image" src="https://github.com/user-attachments/assets/de9a84c7-a00c-4954-bb6e-aff58d7a30ff" />

<img width="1919" height="822" alt="image" src="https://github.com/user-attachments/assets/d9402ae1-8396-4a3f-b4d3-dd9d19d9a87a" />

<img width="1919" height="829" alt="image" src="https://github.com/user-attachments/assets/87751f90-72a7-4403-997e-be22dceec16d" />

<img width="1914" height="833" alt="image" src="https://github.com/user-attachments/assets/1e565bd9-e44c-4553-8575-42d8d3a45e04" />






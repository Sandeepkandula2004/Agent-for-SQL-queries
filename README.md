# 🧠 SQL Chat with Supabase

A conversational Streamlit web app that allows you to interact with your Supabase PostgreSQL database using natural language, powered by LangChain, Groq, and LLaMA3.

## 🚀 Features

- 🤖 LLM Agent using [Groq](https://groq.com/) and LLaMA3 (`llama3-8b-8192`)
- 📦 Connects to Supabase PostgreSQL (via Transaction Pooler)
- 🗨️ Live chat interface using Streamlit
- 🧠 Uses LangChain's `SQLDatabaseToolkit` to interpret your questions into SQL
- 🔄 Keeps chat history during session
- 🛠️ Optional streaming output for better UX

---

## 🛠️ Requirements

- Python 3.9+
- Supabase PostgreSQL instance (with connection details)
- GROQ API Key (get it from https://console.groq.com/)

---

## 📦 Installation

```bash
git clone https://github.com/your-username/sql-chat-supabase.git
cd sql-chat-supabase

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

---

## 🔐 Setup

Create a `.env` file in the project root and add your GROQ API key and Supabase DB password (optional for fallback):

```dotenv
GROQ_API_KEY=your_groq_api_key
SUPABASE_DB_PASSWORD=your_db_password
```

Or use the Streamlit sidebar input fields to provide them securely at runtime.

---

## 🏃 Running the App

```bash
streamlit run app.py
```

Then visit [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🧩 How It Works

1. The app asks for your GROQ API key and Supabase DB password.
2. It uses LangChain's `SQLDatabase` and `SQLDatabaseToolkit` to access the database schema.
3. `ChatGroq` runs LLaMA3 to translate your natural language query into SQL.
4. Results are returned in the chat interface, with previous messages preserved in `st.session_state`.

---

## 🔗 Supabase Connection Format

Make sure your Supabase database is connected using the **transaction pooler** URL format:

```
postgresql://<user>:<password>@<host>:<port>/<db>
```

This app expects:
```python
postgresql://postgres.<your-db-username>:<url-encoded-password>@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres
```

---

## 📋 Example Questions

- "How many users are in the `customers` table?"
- "List all orders placed in the last 7 days."
- "What are the top 5 products by revenue?"

---

## 🧪 Troubleshooting

- **Connection errors**: Check your password and that the transaction pooler is enabled.
- **No response**: Ensure Groq API key is valid and the model is available.
- **Streaming broken**: Disable `streaming=True` if not supported in your setup.

---

## 📄 License

MIT

---

## 🙌 Acknowledgements

- [LangChain](https://www.langchain.com/)
- [Groq](https://groq.com/)
- [Supabase](https://supabase.com/)
- [Streamlit](https://streamlit.io/)

```

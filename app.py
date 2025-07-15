import streamlit as st
from langchain_community.utilities import SQLDatabase
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import urllib.parse
import os

# Load environment variables (optional if using .env for default fallback)
load_dotenv()

# === Page Config ===
st.set_page_config(page_title="🧠 SQL Chat with Supabase", layout="centered")
st.title("💬 Chat with Your Supabase DB")

# === Sidebar Inputs ===
with st.sidebar:
    st.header("🔧 Configuration")
    groq_api_key = st.text_input("🔑 GROQ API Key", type="password", key="groq_key_input")
    db_password = st.text_input("🗝️ Supabase DB Password", type="password", key="db_password_input")

# === Guard Clause ===
if not groq_api_key or not db_password:
    st.warning("Please enter both your GROQ API key and Supabase DB password.")
    st.stop()

# Set GROQ API key as environment variable for LangChain to pick up
os.environ["GROQ_API_KEY"] = groq_api_key

# URL-encode the password to handle special characters
safe_password = urllib.parse.quote_plus(db_password)

# === Build Supabase connection string using the TRANSACTION POOLER ===
# IMPORTANT: Use the hostname and port provided by Supabase for the Transaction Pooler
SUPABASE_DB_URL = f"postgresql://postgres.uuqcbrjvfvwrybsmecpi:{safe_password}@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"

# === Setup LLM and Agent ===
llm = ChatGroq(api_key=groq_api_key, model_name="llama3-8b-8192", streaming=True) # Added streaming=True for better UX
try:
    db = SQLDatabase.from_uri(SUPABASE_DB_URL)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent_executor = create_sql_agent(llm=llm, toolkit=toolkit, verbose=True)
except Exception as e:
    st.error(f"Failed to connect to database: {e}")
    st.stop()

# === Chat History State ===
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Hi! Ask me anything about your Supabase database."}
    ]

# === Show Chat History ===
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# === Chat Input ===
if user_input := st.chat_input("Ask a question about your database..."):
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    try:
        with st.chat_message("assistant"):
            from langchain.callbacks import StreamlitCallbackHandler
            st_callback = StreamlitCallbackHandler(st.container())
            response = agent_executor.invoke(
                {"input": user_input},
                {"callbacks": [st_callback]}
            )
            final_response = response.get("output", "No output from agent.")
            st.session_state.chat_history.append({"role": "assistant", "content": final_response})
            st.write(final_response)
    except Exception as e:
        error_msg = f"❌ Error during agent execution: {str(e)}"
        st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
        with st.chat_message("assistant"):
            st.write(error_msg)







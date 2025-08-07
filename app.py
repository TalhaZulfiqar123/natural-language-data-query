import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType

# Load API Key
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.error("❌ GROQ_API_KEY is not set in the environment variables.")
    st.stop()

# Streamlit page config
st.set_page_config(page_title="CSV Chat Assistant", layout="wide")

# --- Initialize session state for chat ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- CSS Styling ---
st.markdown("""
    <style>
        .title {
            font-size: 42px;
            font-weight: 800;
            color: #1a237e;
        }
        .subtitle {
            font-size: 18px;
            color: #555;
            margin-bottom: 30px;
        }
        .box {
            background-color: #f9f9f9;
            border-radius: 15px;
            padding: 25px;
            margin-top: 20px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.06);
        }
        .chat-box {
            margin-top: 20px;
        }
        .user-msg {
            background-color: #e3f2fd;
            padding: 15px;
            border-radius: 10px;
            font-weight: 500;
            margin-bottom: 10px;
        }
        .ai-msg {
            background-color: #fff3e0;
            padding: 15px;
            border-radius: 10px;
            font-weight: 500;
            border-left: 5px solid #ff9800;
        }
        .footer {
            margin-top: 50px;
            font-size: 14px;
            color: #aaa;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# --- Title & Description ---
st.markdown("<div class='title'>📊 Natural Language CSV Query Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Upload a CSV and ask questions using AI. Built with LangChain + Groq 🚀</div>", unsafe_allow_html=True)

# --- File Upload ---
st.markdown("### 📁 Step 1: Upload Your CSV File")
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")

    # --- Two-column layout ---
    left_col, right_col = st.columns([1, 1])

    # --- LEFT COLUMN: EDA ---
    with left_col:
        st.markdown("### 📈 Basic Data Overview")
        st.markdown("<div class='box'>", unsafe_allow_html=True)

        st.markdown(f"**🔢 Shape:** {df.shape[0]} rows × {df.shape[1]} columns")

        st.markdown("**📋 Column Names:**")
        st.markdown("<ul>" + "".join([f"<li>{col}</li>" for col in df.columns]) + "</ul>", unsafe_allow_html=True)

        st.markdown("**📊 Summary Statistics:**")
        st.dataframe(df.describe(), use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # --- RIGHT COLUMN: Chat with AI ---
    with right_col:
        st.markdown("### 💬 Ask Questions About Your Data")
        user_query = st.text_input("Type your question (e.g., What is the average salary?)")

        if user_query:
            try:
                llm = ChatGroq(
                    groq_api_key=groq_api_key,
                    model_name="llama3-70b-8192"
                )

                agent = create_pandas_dataframe_agent(
                    llm=llm,
                    df=df,
                    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                    allow_dangerous_code=True,
                    verbose=True
                )

                with st.spinner("🤖 Thinking..."):
                    response = agent.run(user_query)

                # Save chat history
                st.session_state.chat_history.append({
                    "user": user_query,
                    "ai": response
                })

            except Exception as e:
                st.error(f"❌ Error: {e}")

        # Show full chat history
        if st.session_state.chat_history:
            st.markdown("<div class='chat-box'>", unsafe_allow_html=True)
            for chat in st.session_state.chat_history:
                st.markdown(f"<div class='user-msg'>👤 <strong>You:</strong> {chat['user']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='ai-msg'>🧠 <strong>AI:</strong> {chat['ai']}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

else:
    st.info("📌 Please upload a CSV file to get started.")

# --- Footer ---
st.markdown("<div class='footer'>✨ Crafted with precision by <strong>Talha Zulfiqar</strong></div>", unsafe_allow_html=True)

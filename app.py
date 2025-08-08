import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType

# --- Load GROQ API Key ---
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.error("❌ GROQ_API_KEY is not set in the environment variables.")
    st.stop()

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="CSV Chat Assistant", layout="wide")

# --- Initialize Chat History in Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Custom CSS Styling ---
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

# --- Page Title and Subtitle ---
st.markdown("<div class='title'>📊 Natural Language CSV Query Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Upload a CSV and ask questions using AI. Built with LangChain + Groq 🚀</div>", unsafe_allow_html=True)

# --- File Upload Section ---
st.markdown("### 📁 Step 1: Upload Your CSV File")
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

# --- If CSV is Uploaded ---
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")

    # --- Create Two-Column Layout ---
    left_col, right_col = st.columns([1, 1])

    # -------------------------------
    # 📊 LEFT COLUMN: EDA INTERFACE
    # -------------------------------
    with left_col:
        st.markdown("### 📈 Basic Data Overview")
        st.markdown("<div class='box'>", unsafe_allow_html=True)

        # --- Always Show First 5 Rows ---
        st.markdown("**🖥️ First 5 Rows of Data:**")
        st.dataframe(df.head(), use_container_width=True)

        # --- EDA Option Selection using Multiselect ---
        eda_options = st.multiselect(
            "Select the types of EDA you want to perform:",
            [
                "Show shape",
                "Show column names",
                "Show summary statistics",
                "Show missing values",
                "Show data types"
            ]
        )

        # --- Show EDA Results Based on Selected Options ---
        if "Show shape" in eda_options:
            st.markdown(f"**🔢 Shape:** {df.shape[0]} rows × {df.shape[1]} columns")

        if "Show column names" in eda_options:
            st.markdown("**📋 Column Names:**")
            st.markdown("<ul>" + "".join([f"<li>{col}</li>" for col in df.columns]) + "</ul>", unsafe_allow_html=True)

        if "Show summary statistics" in eda_options:
            st.markdown("**📊 Summary Statistics:**")
            st.dataframe(df.describe(include='all'), use_container_width=True)

        if "Show missing values" in eda_options:
            st.markdown("**🚨 Missing Values in Each Column:**")
            missing = df.isnull().sum()
            st.dataframe(missing[missing > 0])

        if "Show data types" in eda_options:
            st.markdown("**🧬 Data Types of Columns:**")
            st.dataframe(df.dtypes.reset_index().rename(columns={"index": "Column", 0: "Data Type"}))

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------
    # 🤖 RIGHT COLUMN: CHAT WITH AI
    # ---------------------------------
    with right_col:
        st.markdown("### 💬 Ask Questions About Your Data")
        user_query = st.text_input("Type your question (e.g., What is the average salary?)")

        if user_query:
            try:
                # --- Initialize LLM Agent with LangChain + Groq ---
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

                # --- Store Chat in Session History ---
                st.session_state.chat_history.append({
                    "user": user_query,
                    "ai": response
                })

            except Exception as e:
                st.error(f"❌ Error: {e}")

        # --- Display Chat History ---
        if st.session_state.chat_history:
            st.markdown("<div class='chat-box'>", unsafe_allow_html=True)
            for chat in st.session_state.chat_history:
                st.markdown(f"<div class='user-msg'>👤 <strong>You:</strong> {chat['user']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='ai-msg'>🧠 <strong>AI:</strong> {chat['ai']}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

# --- Show Message if No File Uploaded ---
else:
    st.info("📌 Please upload a CSV file to get started.")

# --- Footer ---
st.markdown("<div class='footer'>✨ Crafted with precision by <strong>Talha Zulfiqar</strong></div>", unsafe_allow_html=True)

import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    ChatPromptTemplate
)
# Custom CSS styling
st.markdown("""
<style>
    /* Enhanced dark theme with better visual hierarchy */
    .main {
        background-color: #0F1117;
        color: #E2E8F0;
    }
    .sidebar .sidebar-content {
        background-color: #1A1E2C;
    }
    .stTextInput textarea {
        color: #ffffff !important;
        background-color: #222736 !important;
        border-radius: 8px !important;
        border: 1px solid #3d4254 !important;
    }
    
    /* Enhanced select box styling */
    .stSelectbox div[data-baseweb="select"] {
        color: white !important;
        background-color: #222736 !important;
        border-radius: 8px !important;
        border: 1px solid #3d4254 !important;
    }
    
    .stSelectbox svg {
        fill: white !important;
    }
    
    .stSelectbox option {
        background-color: #222736 !important;
        color: white !important;
    }
    
    /* Enhanced dropdown menu items */
    div[role="listbox"] div {
        background-color: #222736 !important;
        color: white !important;
    }
    
    /* Card styling for sidebar sections */
    .sidebar-card {
        background-color: #222736;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid #3d4254;
    }
    
    /* Header styling */
    h1, h2, h3 {
        color: #7C3AED !important;
        font-weight: 600 !important;
    }
    
    /* Chat message styling */
    .stChatMessage {
        background-color: #1E2130 !important;
        border-radius: 10px !important;
        padding: 10px !important;
        margin-bottom: 10px !important;
        border: 1px solid #3d4254 !important;
    }
    
    /* Button styling */
    .stButton button {
        border-radius: 8px !important;
        background-color: #7C3AED !important;
        color: white !important;
        border: none !important;
    }
    
    /* Feature badge */
    .feature-badge {
        display: inline-block;
        background-color: rgba(124, 58, 237, 0.2);
        color: #7C3AED;
        padding: 5px 10px;
        border-radius: 5px;
        margin: 5px 0;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)
st.title("⚡ DeepSeek-Code-helper")
st.caption("🚀 Your AI Pair Programmer with Debugging Superpowers")

# Sidebar configuration
with st.sidebar:
    st.header("Configuration")
    selected_model = st.selectbox(
        "Choose Model",
        ["deepseek-r1:1.5b", "deepseek-r1:8b"],
        index=0
    )
    st.divider()
    st.markdown("Model Capabilities")
    st.markdown("""
    <div class='feature-badge'>⚡ Python Expert</div><br>
    <div class='feature-badge'>🔍 Debugging Assistant</div><br>
    <div class='feature-badge'>📊 Code Documentation</div><br>
    <div class='feature-badge'>🏗️ Solution Design</div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown(
        "Built With 💜 by shubh", unsafe_allow_html=True)


# initiate the chat engine

llm_engine = ChatOllama(
    model=selected_model,
    base_url="http://localhost:11434",

    temperature=0.3

)

# System prompt configuration
system_prompt = SystemMessagePromptTemplate.from_template(
    "You are an expert AI coding assistant. Provide concise, correct solutions "
    "with strategic print statements for debugging. Always respond in English."
)

# Session state management
if "message_log" not in st.session_state:
    st.session_state.message_log = [
        {"role": "ai", "content": "Hi! I'm DeepSeek. How can I help you code today? ⚡"}]

# Chat container
chat_container = st.container()

# Display chat messages
with chat_container:
    for message in st.session_state.message_log:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input and processing
user_query = st.chat_input("What code challenge can I help with?")


def generate_ai_response(prompt_chain):
    processing_pipeline = prompt_chain | llm_engine | StrOutputParser()
    return processing_pipeline.invoke({})


def build_prompt_chain():
    prompt_sequence = [system_prompt]
    for msg in st.session_state.message_log:
        if msg["role"] == "user":
            prompt_sequence.append(
                HumanMessagePromptTemplate.from_template(msg["content"]))
        elif msg["role"] == "ai":
            prompt_sequence.append(
                AIMessagePromptTemplate.from_template(msg["content"]))
    return ChatPromptTemplate.from_messages(prompt_sequence)


if user_query:
    # Add user message to log
    st.session_state.message_log.append(
        {"role": "user", "content": user_query})

    # Generate AI response
    with st.spinner("⚡ Processing..."):
        prompt_chain = build_prompt_chain()
        ai_response = generate_ai_response(prompt_chain)

    # Add AI response to log
    st.session_state.message_log.append({"role": "ai", "content": ai_response})

    # Rerun to update chat display
    st.rerun()

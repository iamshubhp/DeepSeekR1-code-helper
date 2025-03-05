import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    ChatPromptTemplate
)

# CSS
st.markdown("""
<style>
    /* Dark Mode Professional Theme */
    :root {
        --bg-primary: #121622;
        --bg-secondary: #1C2331;
        --text-primary: #E0E6ED;
        --accent-color: #3498db;
        --accent-hover: #2980b9;
    }

    /* Global Resets */
    .stApp {
        background-color: var(--bg-primary);
        color: var(--text-primary);
        font-family: 'Inter', 'system-ui', sans-serif;
    }

    /* Sidebar Styling */
    .css-1aumxhk {
        background-color: var(--bg-secondary);
        border-right: 1px solid #2C3E50;
        padding: 20px;
    }

    /* Title Styling */
    .stTitle {
        color: var(--text-primary);
        text-align: center;
        font-weight: 700;
        letter-spacing: -1px;
    }

    /* Chat Input */
    .stTextInput > div > div > input {
        background-color: var(--bg-secondary);
        border: 2px solid var(--accent-color);
        color: var(--text-primary);
        border-radius: 8px;
        padding: 12px;
        transition: all 0.3s ease;
    }

    .stTextInput > div > div > input:focus {
        outline: none;
        border-color: var(--accent-hover);
        box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.2);
    }

    /* Chat Messages */
    .stChatMessage {
        background-color: var(--bg-secondary);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        position: relative;
    }

    .stChatMessage[data-role="ai"] {
        border-left: 4px solid var(--accent-color);
    }

    .stChatMessage[data-role="user"] {
        border-left: 4px solid #2ECC71;
    }

    /* Buttons and Selects */
    .stButton > button {
        background-color: var(--accent-color);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 15px;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background-color: var(--accent-hover);
        transform: translateY(-2px);
    }

    .stSelectbox > div > div > select {
        background-color: var(--bg-secondary);
        color: var(--text-primary);
        border: 2px solid var(--accent-color);
        border-radius: 6px;
    }

    /* Capabilities List */
    .stMarkdown ul {
        list-style: none;
        padding: 0;
    }

    .stMarkdown ul li {
        background-color: var(--bg-primary);
        margin: 8px 0;
        padding: 10px;
        border-radius: 6px;
        display: flex;
        align-items: center;
        transition: background-color 0.3s ease;
    }

    .stMarkdown ul li:hover {
        background-color: var(--bg-secondary);
    }
</style>
""", unsafe_allow_html=True)

st.title("DeepSeek - Code Helper")
st.caption("Your AI Pair Programmer with Debugging Superpowers")


with st.sidebar:
    st.header("Configuration")
    selected_model = st.selectbox(
        "Choose Model",
        ["deepseek-r1:1.5b", "deepseek-r1:3b"],
        index=0
    )
    st.divider()
    st.markdown("### Model Capabilities")
    st.markdown("""
    - Python Expert
    - Debugging Assistant
    - Code Documentation
    - Solution Design
    """)
    st.divider()
    st.markdown(
        "Built with love by shubh <3")


# initiate the chat engine

llm_engine = ChatOllama(
    model=selected_model,
    base_url="http://localhost:11434",

    temperature=0.3

)


system_prompt = SystemMessagePromptTemplate.from_template(
    "You are an expert AI coding assistant. Provide concise, correct solutions "
    "with strategic print statements for debugging. Always respond in English."
)


if "message_log" not in st.session_state:
    st.session_state.message_log = [
        {"role": "ai", "content": "Hi! I'm DeepSeek. How can I help you code today? 💻"}]


chat_container = st.container()


with chat_container:
    for message in st.session_state.message_log:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


user_query = st.chat_input("Type your coding question here...")


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

    st.session_state.message_log.append(
        {"role": "user", "content": user_query})

    # Generate AI response
    with st.spinner("🧠 Processing..."):
        prompt_chain = build_prompt_chain()
        ai_response = generate_ai_response(prompt_chain)

    st.session_state.message_log.append({"role": "ai", "content": ai_response})

    st.rerun()

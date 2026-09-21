import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()
st.set_page_config(page_title="AI Chatbox",layout="centered")
if "messages" not in st.session_state:
    st.session_state.messages=[]
st.title("AI Chatbox")
st.caption("AI Chatbox")
with st.sidebar:
    st.header("Settings")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    model = st.selectbox(
        "Select Model",
        ["openai/gpt-oss-120b","openai/gpt-oss-20b"]
    )
    if st.button("Download chat"):
        if st.session_state.get("messages"):
            chat_text=""
            for msg in st.session_state.messages:
                role="you" if msg["role"]=="user" else "AI"
                chat_text += f"{role}:{msg['content']}\n\n"
            st.download_button(
                label="Click to Download",
                data=chat_text,
                file_name="chat_history.txt",
                mime="text/plain"
            )
        else:
            st.warning("No chat to download")
    st.markdown("---")
    st.subheader("Chat History")
    if len(st.session_state.messages)>0:
        for msg in st.session_state.messages:
            role="You" if msg["role"] =="user" else "AI"
            st.caption(f"{role}:{msg['content'][:50]}...")
    else:
        st.caption("No Messages Yet")
    dark_mode=st.toggle("Dark Mode",value=False)
    st.markdown("---")
    st.markdown("**Model:** openai/gpt-oss-20b")
if dark_mode:
    st.markdown("""
            <style>
                .stApp
                {
                background-color: black;
                color : white;
                }
                section[data-testid="stSidebar"]
                {
                    background-color:grey;
                }
                div[data-testid="stChatInput"]
                {
                    background-color: dimgrey;
                }
                div[data-testid="stChatInput"] textarea{
                background-color: dimgrey
                color: white;
                }
                div[data-testid="stBottom"]
                {
                background-color: black;
                }
            </style>
        """,unsafe_allow_html=True)
else:
    st.markdown("""
            <style>
                .stApp
                {
                    background-color: white;
                    color : black;
                }
                section[data-testid="stSidebar"]
                {
                    background-color:grey;
                }
                div[data-testid="stChatInput"] textarea {
                background-color: white;
                color: black;
                }
                div[data-testid="stBottom"]
                {
                    background-color: white;
                }
            </style>
        """,unsafe_allow_html=True)
if "messages" not in st.session_state:
    st.session_state.messages = []
if len(st.session_state.messages) == 0:
    st.info(" Hello! i'm AI , Ask me")
    st.markdown("**Try these questions:**")
    col1, col2=st.columns(2)
    with col1:
        if st.button("What is Artificial Intelligence?"):
            st.session_state.messages.append({"role":"user","content":"What is Artificial Inteligence?"})
            st.session_state.generate=True
            st.rerun()
        if st.button("Explain Machine Learning"):
            st.session_state.messages.append({"role":"user","content":"Explain machine learning"})
            st.session_state.generate=True
            st.rerun()
    with col2:
        if st.button("What is Data Science?"):
            st.session_state.messages.append({"role":"user","content":"What is Data Science?"})
            st.session_state.generate=True
            st.rerun()
        if st.button("Difference between AI and ML"):
            st.session_state.messages.append({"role":"user","content":"Difference between AI and ML"})
            st.session_state.generate=True
            st.rerun()
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
prompt = st.chat_input("Type your message here...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.generate=True
if st.session_state.get("generate") and st.session_state.messages and st.session_state.messages[-1]["role"]=="user":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                client = Groq(api_key=os.getenv("GROQ_API_KEY"))
                api_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "system", "content": "You are a helpful AI assistant powered by openai/gpt-oss-20b Do Not refer to yourself as ChatGPT or OpenAI."}
                    ] + st.session_state.messages + api_messages,
                    temperature=0.7,
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error: {e}")
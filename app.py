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
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                client = Groq(api_key=os.getenv("GROQ_API_KEY"))
                api_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[{"role": "system", "content": "You are a helpful AI assistant powered by openai/gpt-oss-20b Do Not refer to yourself as ChatGPT or OpenAI."}
                    ] + st.session_state.messages,
                    temperature=0.7,
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error: {e}")
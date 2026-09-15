import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()
st.set_page_config(page_title="AI Chatbox",layout="centered")
st.title("AI Chatbox")
st.caption("AI Chatbox")
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()
if "messages" not in st.session_state:
    st.session_state.messages = []
if len(st.session_state.messages) == 0:
    st.info(" Hello! i'm AI , Ask me")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
if prompt := st.chat_input("Message AI Chatbox..."):
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
                    messages=api_messages,
                    temperature=0.7,
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error: {e}")
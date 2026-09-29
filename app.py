import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
from pypdf import PdfReader
load_dotenv()
st.set_page_config(page_title="AI Chatbox",layout="centered")
if "chats" not in st.session_state:
    st.session_state.chats={"Chat 1":[]}
if "current_chat" not in st.session_state:
    st.session_state.current_chat="Chat 1"
if "messages" not in st.session_state:
    st.session_state.messages=st.session_state.chats[st.session_state.current_chat]
if "uploaded_files_list" not in st.session_state:
    st.session_state.uploaded_files_list=[]
st.title("AI Chatbox")
st.caption("AI Chatbox")
with st.sidebar:
    st.header("Settings")
    if st.button("New Chat"):
        new_chat_name=f"Chat {len(st.session_state.chats)+1}"
        st.session_state.chats[new_chat_name]=[]
        st.session_state.current_chat=new_chat_name
        st.session_state.messages=st.session_state.chats[new_chat_name]
        st.rerun()
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.subheader("Chat History")
    for chat_name in st.session_state.chats:
        if st.button(chat_name,key=f"chat_{chat_name}"):
            st.session_state.current_chat=chat_name
            st.session_state.messages=st.session_state.chats[chat_name]
            st.rerun()
    model = st.selectbox(
        "Select Model",
        ["openai/gpt-oss-120b","openai/gpt-oss-20b"]
    )
    temperature=st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Low = Precise answer | High = Creative answers"
    )
    st.markdown("---")
    st.subheader("AI Personality")
    system_prompt = st.text_area(
        "System Prompt",
        value="You are a helpful and friendly AI assistant. Give clear and simple answers.",
        height=100,
        help="Change the AI's behavior and personality here"
    )
    st.markdown("---")
    st.subheader("Upload Document")
    uploaded_files = st.file_uploader(
        "Upload PDF or Text file",
        type=["pdf","txt","docx","csv","md","json","xlsx","xls","py","html","xml","log","rtf","jpg","jpeg","png","webp","bmp","gif","ppt","pptx","odt","ods"],
        accept_multiple_files=True,
        key="file_uploader"
    )
    if uploaded_files:
        for file in uploaded_files:
            if file.name not in [f.name for f in st.session_state.uploaded_files_list]:
                st.session_state.uploaded_files_list.append(file)
    if st.session_state.uploaded_files_list:
        st.write("**Uploaded Files:**")
        for i, file in enumerate(st.session_state.uploaded_files_list):
            col1, col2=st.columns([4,1])
            with col1:
                st.write(f"{file.name}")
            with col2:
                if st.button("X",key=f"remove_{i}"):
                    st.session_state.uploaded_files_list.pop(i)
                    st.rerun()
        all_content=""
        for file in st.session_state.uploaded_files_list:
            if file.name.endswith((".txt",".md",".py",".json",".html",".xml",".log",".csv",".rtf")):
                content = file.read().decode("utf-8")
                all_content += f"\n\n---File: {file.name}---\n{content}"
                file.seek(0)
            elif file.name.endswith(".pdf"):
                reader=PdfReader(file)
                content=""
                for page in reader.pages:
                    content +=page.extract_text() or ""
                all_content += f"\n\n---File: {file.name}---\n{content}"
                file.seek(0)
            else: 
                all_content += f"\n\n---File: {file.name}---\n(This file will be supported soon.)"
        st.session_state.file_content=all_content
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
    st.subheader("Chat Stats")
    total=len(st.session_state.get("messages",[]))
    user_msgs=len([m for m in st.session_state.get("messages",[]) if m["role"]=="user"])
    ai_msgs=len([m for m in st.session_state.get("messages",[]) if m["role"]=="assistant"])
    st.write(f"**Total Messages:** {total}")
    st.write(f"**Your Messages:** {user_msgs}")
    st.write(f"AI Messages:** {ai_msgs}")
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
    st.session_state.chats[st.session_state.current_chat]=st.session_state.messages
    st.session_state.generate=True
    st.rerun()
if st.session_state.get("generate") and st.session_state.messages and st.session_state.messages[-1]["role"]=="user":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                client = Groq(api_key=os.getenv("GROQ_API_KEY"))
                final_system_prompt = system_prompt
                if "file_content" in st.session_state and st.session_state.file_content:
                    final_system_prompt += f"\n\nHere is the content of the uploaded document:\n\n{st.session_state.file_content[:8000]}"
                api_messages = [{"role":"system","content":"You are a helpful AI assistant powered by openai/gpt-oss-20b Do Not refer to yourself as ChatGPT or OpenAI.\n\n" + final_system_prompt}] + [{"role":m["role"],"content":m["content"]} for m in st.session_state.messages]
                response = client.chat.completions.create(
                    model=model,
                    messages=api_messages,
                    temperature=temperature,
                    stream=True
                )
                reply = ""
                response_placeholder = st.empty()
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        reply += chunk.choices[0].delta.content
                        response_placeholder.markdown(reply + "| ")
                response_placeholder.markdown(reply)
                st.download_button(
                    label="Copy Response",
                    data=reply,
                    file_name="response.txt",
                    mime="text/plain",
                    key=f"copy_{len(st.session_state.messages)}"
                )
                st.session_state.messages.append({"role":"assistant","content":reply})
                st.session_state.chats[st.session_state.current_chat]=st.session_state.messages
            except Exception as e:
                st.error(f"Error: {e}")
                st.write(e)
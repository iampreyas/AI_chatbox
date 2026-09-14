import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()
st.set_page_config
(
	page_title="AI Chatbox",
	layout="centered"
)
st.markdown
("""
	<style>
	.stApp
	{
		max-width:800px;
		margin:auto;
	}
	</style>
""",unsafe_allow_html=True)
st.title("AI Chatbox")
st.caption("Your Personal AI")
if "messages" not in st.session_state:
	st.session_state.messages=[]
for message in st.session_state.message:
	with st.chat_message(message["role"]):
		st.markdown(message["content"])
if prompt:=st.chat_input("Message AI Chatbox.."):
	st.session_state.message.append({"role":"user","content":prompt})
	with st.chat_message("user"):
		st.markdown(prompt)
	with st.chat_message("assistant"):
		with st.spinner("Thinking.."):
			try:
				client=Groq(api_key=os.getenv("GROQ_API_KEY"))
				api_message=[{"role":m["role"], "content": m["content"]}
				for m in st.session_state.messages]
				response=client.chat.completion.create
				(
					model="llama-3.3-70b-versatile",
					message=api_messages,
					temperature=0.7,
				)
				reply=response.choices[0].message.content
				st.markdown(reply)
				st.session_state.message.append({"role":"assistant","content":reply})
			expect Exception as e:
				st.error(f"Error:{e}")
				st.info("please check your GROQ_API_KEY in .env file")
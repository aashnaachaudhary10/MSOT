import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("API Key not found. Please add GEMINI_API_KEY to your .env file.")
    st.stop()

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(page_title="Memory Vault Chatbot", page_icon="🤖")

st.title("Memory Vault Chatbot")
st.write("A chatbot that remembers your conversation using Session State.")

personality = st.selectbox(
    "Choose AI Personality",
    ["Teacher", "Programmer", "Friend"]
)

prompts = {
    "Teacher": "You are a helpful teacher. Explain everything in simple language.",
    "Programmer": "You are an experienced programmer. Help users with coding questions.",
    "Friend": "You are a friendly buddy. Reply casually and positively."
}

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if user_message := st.chat_input("Say something..."):
    with st.chat_message("user"):
        st.write(user_message)
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )
    full_prompt = prompts[personality] + "\nUser: " + user_message

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            response = model.generate_content(full_prompt)

            st.write(response.text)
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response.text
        }
    )
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()
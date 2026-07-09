import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(page_title="AI Multiverse", page_icon="🤖")

st.title("AI Multiverse Chatbot")
st.write("Choose an AI personality and start chatting!")

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

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            full_prompt = prompts[personality] + "\n\nUser: " + user_input

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
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API Key not found!")
    st.stop()

@st.cache_resource
def load_model():
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")

model = load_model()

st.set_page_config(
    page_title="AI Visual Novel",
    page_icon="📖",
    layout="wide"
)

st.title("AI Multi-Modal Visual Novel")
st.write("Create your own AI-powered adventure!")

st.sidebar.title("Story Settings")

genre = st.sidebar.selectbox(
    "Choose Genre",
    [
        "Fantasy",
        "Sci-Fi",
        "Horror",
        "Mystery"
    ]
)

art_style = st.sidebar.selectbox(
    "Choose Art Style",
    [
        "Anime",
        "Realistic",
        "Pixel Art",
        "Watercolor"
    ]
)


if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

st.subheader("Start Your Adventure")

st.info(
    f"""
Genre : {genre}

Art Style : {art_style}

Press the button below to begin your AI story.
"""
)

if st.button("Start Story"):
    st.success("Story generation will begin in Part 2!")
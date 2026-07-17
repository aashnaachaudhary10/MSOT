import streamlit as st
import requests
import random
from PIL import Image
from io import BytesIO
from urllib.parse import quote


st.set_page_config(page_title="AI Image Studio", page_icon="🎨")

st.title("AI Image Studio")
st.write("Generate AI images using Pollinations AI")

st.sidebar.header("Image Settings")

width = st.sidebar.slider("Width", 256, 1024, 512, 64)
height = st.sidebar.slider("Height", 256, 1024, 512, 64)

art_style = st.sidebar.selectbox(
    "Art Style",
    ["Realistic", "Anime", "Cyberpunk", "Fantasy", "Watercolor"]
)

magic_enhance = st.sidebar.checkbox(" Enable Magic Enhance")


prompt = st.text_input("Enter your image prompt")

surprise_prompts = [
    "An astronaut riding a horse on Mars",
    "A cyberpunk street food vendor in Tokyo",
    "A giant robot serving coffee in Paris",
    "A dragon flying over the Himalayas",
    "A futuristic underwater city"
]

col1, col2 = st.columns(2)

with col1:
    generate_btn = st.button("🚀 Generate Image")

with col2:
    surprise_btn = st.button("🎲 Surprise Me!")


if surprise_btn:
    prompt = random.choice(surprise_prompts)
    st.info(f"🎲 Surprise Prompt: {prompt}")
    generate_btn = True

if generate_btn:

    if prompt.strip() == "":
        st.warning("Please enter a prompt.")
    else:
        full_prompt = f"{prompt}, {art_style} style"

        if magic_enhance:
            full_prompt += ", masterpiece, 8k resolution, highly detailed, trending on artstation, unreal engine 5 render"

        encoded_prompt = quote(full_prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}"

        with st.spinner("Generating image..."):
            response = requests.get(url)

        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))

            st.image(image, caption="Generated Image", use_container_width=True)
            st.download_button(
                label="Download Image",
                data=response.content,
                file_name=f"{art_style}_image.png",
                mime="image/png"
            )
        else:
            st.error("Failed to generate image.")
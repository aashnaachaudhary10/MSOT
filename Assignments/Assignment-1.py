import streamlit as st
st.set_page_config(page_title="The Identity Echo Interface", page_icon="🤖")
st.title("The Identity Echo Interface")
st.write("Enter your name and message below, then click **Transmit** to send your message.")
user_name = st.text_input("Enter your Name")
user_message = st.text_input("Enter your Message")

if st.button("Transmit"):

    if user_name.strip() == "":
        st.error("Please provide your name.")

    elif user_message.strip() == "":
        st.warning("Please type a message to transmit.")
    else:
        st.success(
            f"Transmission successful! Greetings, {user_name}. "
            f"We received your message: {user_message}"
        )

        total_characters = len(user_message)
        token_count = total_characters / 4

        st.info(
            f"System Check: Your message will consume approximately "
            f"{token_count:.2f} tokens from our context window."
        )
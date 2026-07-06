import streamlit as st

st.set_page_config(page_title="Calculator", page_icon="🧮", layout="centered")

st.title("🧮 Streamlit Calculator")
num1 = st.number_input("Enter first number", value=0.0)
num2 = st.number_input("Enter second number", value=0.0)

operation = st.selectbox(
    "Choose an operation",
    ("Addition", "Subtraction", "Multiplication", "Division")
)

result = None

if st.button("Calculate"):
    if operation == "Addition":
        result = num1 + num2

    elif operation == "Subtraction":
        result = num1 - num2

    elif operation == "Multiplication":
        result = num1 * num2

    elif operation == "Division":
        if num2 != 0:
            result = num1 / num2
        else:
            st.error("Cannot divide by zero")

    if result is not None:
        st.success(f"Result: {result}")

st.markdown("---")
st.caption("Built with Streamlit")
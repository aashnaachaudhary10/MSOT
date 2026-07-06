#BASICALLY STREAMLIT IS FRAMEWORK OF PYTHON WHICH IS USED FOR DEVELOPINF WEBSITES IF WE DONT KNOW WEB DEVELOPMENT IN PURE PYTHON SO STARTING WITH THIS.

import streamlit as st 
st.title ("Hello Chai App")
st.subheader("Brewed with streamlit")
st.text("Welcome to your first interactive app")
st.write("Choose your fav , variety of chai")

chai=st.selectbox("Your fav chai:",["Masala chai","Lemon Tea","Adrak Chai","Kesar Chai"])
st.write(f"Your choose {chai}.Excellent choise")
st.success("Your chai has been brewed")
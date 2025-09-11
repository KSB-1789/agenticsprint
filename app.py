import streamlit as st

# Title of app
st.title("AgenticSprint Prototype")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Ask AI"])

# Home Page
if page == "Home":
    st.write("👋 Welcome to our AI project!")
    st.write("This is the prototype frontend.")

# Ask AI Page
elif page == "Ask AI":
    user_input = st.text_input("Enter your question:")
    if st.button("Submit"):
        st.write("🔮 Placeholder Answer: This will come from our backend.")

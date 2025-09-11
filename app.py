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
    st.header("Chat with our AI 🤖")

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Display existing chat messages
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input box
    if prompt := st.chat_input("Type your question..."):
        # Save user message
        st.session_state["messages"].append({"role": "user", "content": prompt})
        
        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Placeholder AI response
        import requests

        # inside Ask AI section, after user enters prompt
        response = requests.post("http://127.0.0.1:8000/ask", json={"question": prompt})

        if response.status_code == 200:
            answer = response.json()["answer"]
        else:
            answer = "⚠️ Backend error."

        st.session_state["messages"].append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)

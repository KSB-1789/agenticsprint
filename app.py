import streamlit as st
import requests
import time

st.set_page_config(page_title="AgenticSprint Prototype", layout="centered")


# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Ask AI"])
mode = st.sidebar.radio("Demo Mode", ["Real", "Dummy"])

# --- Home Page ---
if page == "Home":
    st.title("👋 Welcome to AgenticSprint Prototype")
    st.write("This is our hackathon-ready AI project frontend.")
    st.info("Use the sidebar to switch pages and toggle between Real/Dummy modes.")

# --- Ask AI Page ---
elif page == "Ask AI":
    st.header("💬 Chat with our AI Assistant")

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Display chat history
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input
    if prompt := st.chat_input("Type your question..."):
        # Save user message
        st.session_state["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Thinking..."):
            time.sleep(1)

            if mode == "Dummy":
                answer = f"🤖 Dummy Response: '{prompt[:40]}...' processed successfully!"
            else:
                try:
                    response = requests.post(
                        "http://127.0.0.1:8000/predict",
                        json={"input": prompt},
                        timeout=10
                    )
                    if response.status_code == 200:
                        data = response.json()
                        answer = data.get("output", "⚠️ No output field in response.")
                    else:
                        answer = f"⚠️ Backend error: {response.status_code}"
                except Exception as e:
                    answer = f"⚠️ Could not connect to backend.\n\nDetails: {e}"

        # Save + display assistant response
        st.session_state["messages"].append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)

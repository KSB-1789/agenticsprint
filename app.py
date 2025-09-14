import streamlit as st
import requests
import time

st.set_page_config(page_title="AgenticSprint Prototype", layout="centered")

st.markdown(
    """
    <style>
    /* Hide default Streamlit header */
    [data-testid="stHeader"] {
        display: none;
    }
    /* Main app background */
    body, .main, [data-testid="stAppViewContainer"] {
        background-color: #0F172A !important;  /* Slate-900 for premium dark look */
        margin: 0 !important;
    }
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #020617 !important;  /* Slate-950 */
        padding: 1.5rem !important;
        box-shadow: 2px 0 5px rgba(0,0,0,0.3) !important;
        position: relative;
        min-height: 100vh;
    }
    /* Block container padding */
    .block-container {
        padding-top: 1rem !important;  /* Adjusted to account for removed header */
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1200px !important;
        margin-top: 0 !important;
    }
    /* Headings */
    h1, h2, h3 {
        color: #F1F5F9 !important;  /* Slate-100 */
        font-family: 'Inter', sans-serif !important;
    }
    /* File uploader */
    .stFileUploader {
        margin-bottom: 1.5rem !important;
        background-color: #020617 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        border: 1px solid #1E293B !important;
    }
    /* Metrics */
    .stMetric {
        background-color: #1E293B !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3) !important;
        color: #F1F5F9 !important;
    }
    /* Captions */
    .stCaption {
        color: #94A3B8 !important;  /* Slate-400 */
    }
    /* Spinner */
    div.stSpinner > div {
        color: #F1F5F9 !important;
    }
    /* Sidebar upload spacer */
    .sidebar-upload {
        margin-top: 2rem;
        margin-bottom: 2rem;
    }
    /* Pin powered by to bottom of sidebar */
    .sidebar-bottom {
        position: absolute;
        bottom: 2rem;
        left: 1.5rem;
        width: 80%;
        color: #94A3B8;
        font-size: 0.95rem;
        text-align: left;
    }
    /* Chat message styling for dark theme */
    .stChatMessage {
        background-color: #1E293B !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        color: #F1F5F9 !important;
    }
    /* Chat input */
    .stChatInput input {
        background-color: #020617 !important;
        color: #F1F5F9 !important;
        border: 1px solid #1E293B !important;
    }
    /* Ensure content adjusts when sidebar collapses */
    @media (max-width: 640px) {
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        section[data-testid="stSidebar"] {
            display: block; /* Ensure sidebar remains visible on small screens */
            width: 100% !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
                        "http://127.0.0.1:8000/ask",
                        json={"question": prompt},  # matches Pydantic model
                        timeout=15
                    )
                    if response.status_code == 200:
                        data = response.json()
                        answer = data.get("answer", "⚠️ No 'answer' field in response.")
                    else:
                        answer = f"⚠️ Backend error: {response.status_code}"
                except Exception as e:
                    answer = f"⚠️ Could not connect to backend.\n\nDetails: {e}"

        # Save + display assistant response
        st.session_state["messages"].append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)

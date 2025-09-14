import streamlit as st
import requests
import time
import pandas as pd
import altair as alt

st.set_page_config(page_title="AgenticSprint CFO Dashboard", layout="wide")

# --- Dark Theme Custom CSS ---
st.markdown(
    """
    <style>
    [data-testid="stHeader"] {
        display: none;
    }
    body, .main, [data-testid="stAppViewContainer"] {
        background-color: #0F172A !important;
        margin: 0 !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #020617 !important;
        padding: 1.5rem !important;
        box-shadow: 2px 0 5px rgba(0,0,0,0.3) !important;
        position: relative;
        min-height: 100vh;
    }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1200px !important;
        margin-top: 0 !important;
    }
    h1, h2, h3 {
        color: #F1F5F9 !important;
        font-family: 'Inter', sans-serif !important;
    }
    .stFileUploader {
        margin-bottom: 1.5rem !important;
        background-color: #020617 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        border: 1px solid #1E293B !important;
    }
    .stMetric {
        background-color: #1E293B !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3) !important;
        color: #F1F5F9 !important;
    }
    .stCaption {
        color: #94A3B8 !important;
    }
    div.stSpinner > div {
        color: #F1F5F9 !important;
    }
    .stChatMessage {
        background-color: #1E293B !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        color: #F1F5F9 !important;
    }
    .stChatInput input {
        background-color: #020617 !important;
        color: #F1F5F9 !important;
        border: 1px solid #1E293B !important;
    }
    @media (max-width: 640px) {
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        section[data-testid="stSidebar"] {
            display: block;
            width: 100% !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Sidebar ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Dashboard"])
mode = st.sidebar.radio("Demo Mode", ["Real", "Dummy"])
uploaded_file = st.sidebar.file_uploader("Upload financial CSV/XLSX", type=["csv", "xlsx"])

# --- Home Page ---
if page == "Home":
    st.title("👋 Welcome to AgenticSprint CFO Dashboard")
    st.write("Hackathon-ready AI CFO assistant prototype.")
    st.info("Upload a financial file, switch between Real/Dummy mode, and explore KPIs, charts, and advisory.")

# --- Dashboard Page ---
elif page == "Dashboard":
    st.header("💼 CFO Dashboard")

    # --- Tabs ---
    tabs = st.tabs(["Chat", "Metrics", "Charts", "Advisory"])

    # --- Chat Tab ---
    with tabs[0]:
        st.subheader("💬 Chat with AI Assistant")
        if "messages" not in st.session_state:
            st.session_state["messages"] = []

        for msg in st.session_state["messages"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if prompt := st.chat_input("Type your question..."):
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
                            json={"question": prompt},
                            timeout=15
                        )
                        if response.status_code == 200:
                            data = response.json()
                            answer = data.get("answer", "⚠️ No 'answer' field in response.")
                        else:
                            answer = f"⚠️ Backend error: {response.status_code}"
                    except Exception as e:
                        answer = f"⚠️ Could not connect to backend.\n\nDetails: {e}"

            st.session_state["messages"].append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.markdown(answer)

    # --- Metrics Tab ---
    with tabs[1]:
        st.subheader("📊 Key Financial Metrics")
        if uploaded_file:
            try:
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)

                st.markdown("### 📂 Uploaded Data Preview")
                st.dataframe(df.head())
            except Exception as e:
                st.error(f"Could not read file: {e}")
                df = None
            else:
                if mode == "Dummy":
                    kpis = {
                        "Profit": 50000,
                        "Debt Ratio": 0.35,
                        "Burn Rate": 12000,
                        "Runway Months": 8
                    }
                else:
                    try:
                        kpis_payload = {
                            "revenue": float(df["Revenue"].sum()),
                            "expenses": float(df["Expenses"].sum()),
                            "liabilities": float(df["Liabilities"].sum()),
                            "burn_rate": float(df["BurnRate"].sum()),
                            "runway_months": 6
                        }
                        response = requests.post("http://127.0.0.1:8000/analyze", json=kpis_payload, timeout=10)
                        if response.status_code == 200:
                            kpis = response.json()
                        else:
                            st.error("Backend error for /analyze")
                            kpis = {}
                    except Exception as e:
                        st.error(f"Could not analyze file: {e}")
                        kpis = {}

                if kpis:
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Profit", kpis.get("profit", "N/A"))
                    col2.metric("Debt Ratio", kpis.get("debt_ratio", "N/A"))
                    col3.metric("Burn Rate", kpis.get("burn_rate", "N/A"))
                    col4.metric("Runway Months", kpis.get("runway_months", "N/A"))
        else:
            st.info("Upload a financial CSV/XLSX file to see metrics.")

    # --- Charts Tab ---
    with tabs[2]:
        st.subheader("📈 Financial Charts")
        if uploaded_file:
            if mode == "Dummy":
                expenses_data = pd.DataFrame({
                    "Category": ["R&D", "Marketing", "Operations", "Salaries"],
                    "Amount": [3000, 2000, 4000, 5000]
                })
                runway_data = pd.DataFrame({
                    "Month": ["Jan", "Feb", "Mar", "Apr", "May"],
                    "Runway": [8, 7.5, 7, 6.5, 6]
                })
            else:
                expenses_data = pd.DataFrame({
                    "Category": ["Dummy1", "Dummy2"],
                    "Amount": [100, 200]
                })
                runway_data = pd.DataFrame({
                    "Month": ["Jan", "Feb"],
                    "Runway": [6, 5.5]
                })

            st.markdown("**Expenses Breakdown**")
            pie = alt.Chart(expenses_data).mark_arc().encode(
                theta="Amount",
                color="Category"
            )
            st.altair_chart(pie, use_container_width=True)

            st.markdown("**Runway Projection**")
            line = alt.Chart(runway_data).mark_line(point=True).encode(
                x="Month",
                y="Runway"
            )
            st.altair_chart(line, use_container_width=True)
        else:
            st.info("Upload a financial CSV/XLSX file to see charts.")

    # --- Advisory Tab ---
    with tabs[3]:
        st.subheader("📝 Advisory")
        if uploaded_file:
            if mode == "Dummy":
                advice_text = "✅ Profit is positive. ⚠️ Runway is short (6 months). ✅ Debt ratio is acceptable."
            else:
                try:
                    response = requests.post("http://127.0.0.1:8000/advisory", json=kpis_payload, timeout=10)
                    if response.status_code == 200:
                        advice_text = response.json().get("advice", "⚠️ No advice received")
                    else:
                        advice_text = "⚠️ Backend error for /advisory"
                except Exception as e:
                    advice_text = f"⚠️ Could not connect to backend: {e}"
            st.info(advice_text)
        else:
            st.info("Upload a financial CSV/XLSX file to get advisory recommendations.")

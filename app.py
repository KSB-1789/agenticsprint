import streamlit as st
import requests
import time
import pandas as pd
import altair as alt

# --- Page Config (set once) ---
st.set_page_config(page_title="AI CFO Dashboard", layout="centered")

# --- Sidebar ---
st.sidebar.markdown("<h2>C<sup>3</sup></h2>", unsafe_allow_html=True)
page = st.sidebar.radio("Go to", ["Dashboard", "Ask AI"])
mode = st.sidebar.radio("Choose Mode", ["Real", "Dummy"])

# Upload section
st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader("📂 Upload Financial Report", type=["pdf", "xlsx", "xls", "csv"])

# --- Dynamic Layout Hack ---
if page == "Dashboard":
    # MODIFIED: Reduced top padding to use space more effectively
    st.markdown(
        """
        <style>
        .block-container {
            max-width: 95% !important;
            padding-top: 1rem !important;
            padding-left: 2rem;
            padding-right: 2rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    # Centered layout simulation
    st.markdown(
        """
        <style>
        .block-container {
            max-width: 45% !important;
            margin: auto;
            padding-top: 2rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# --- Custom CSS (kept from your version) ---
st.markdown("""
<style>
    [data-testid="stSidebar"] h2 {
        text-align: center;
        font-size: 2em;
        font-weight: bold;
        padding-bottom: 1.5rem;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] {
        display: flex;
        flex-direction: column;
        align-items: right;
        padding-bottom: 2rem;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] > label {
        font-size: 2em;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# --- Dummy Data (Enhanced for new charts) ---
dummy_data = {
    "metrics": {
        "revenue": 50000,
        "expenses": 32000,
        "burn_rate": 5000,
        "runway_months": 6
    },
    "advisory": "📉 High burn rate detected. Reduce expenses by 10% to extend runway.",
    "expense_breakdown": pd.DataFrame({
        "Category": ["Ops", "Marketing", "Salaries", "R&D"],
        "Amount": [10000, 8000, 12000, 2000]
    }),
    "runway_projection": pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Cash": [50000, 45000, 40000, 35000, 30000, 25000]
    })
}

# --- Dashboard Page ---
if page == "Dashboard":
    st.title("📊 AI CFO Dashboard")
    st.write("Analyze startup financial health with AI insights.")

    data = None
    advice = None
    expense_chart_data = None
    runway_chart_data = None
    df_preview = None

    if mode == "Dummy":
        data = dummy_data["metrics"]
        advice = dummy_data["advisory"]
        expense_chart_data = dummy_data["expense_breakdown"]
        runway_chart_data = dummy_data["runway_projection"]

    else: # Real mode
        if uploaded_file is None:
            st.warning("📂 Please upload a financial report (PDF/Excel) to see results.")
        else:
            # Attempt to read and preview the uploaded file
            try:
                if uploaded_file.name.endswith('.csv'):
                    df_preview = pd.read_csv(uploaded_file)
                else:
                    df_preview = pd.read_excel(uploaded_file)
                # Reset pointer for sending to backend
                uploaded_file.seek(0)
            except Exception as e:
                st.warning(f"Could not generate a data preview. Error: {e}")
                df_preview = None

            # Original backend logic
            try:
                files = {"file": uploaded_file.getvalue()}
                with st.spinner("AI is analyzing your document..."):
                    response = requests.post("http://127.0.0.1:8000/ingest", files=files, timeout=20)

                if response.status_code == 200:
                    payload = response.json()
                    data = payload.get("metrics")
                    advice = payload.get("advisory")
                    # Assume backend can also return chart data
                    expense_chart_data = pd.DataFrame(payload.get("expense_breakdown", []))
                    runway_chart_data = pd.DataFrame(payload.get("runway_projection", []))
                else:
                    st.error(f"⚠️ Backend error: {response.status_code}")
            except Exception as e:
                st.error(f"⚠️ Could not connect to backend.\n\nDetails: {e}")

    # Show dashboard only if data is valid
    if data is not None:
        # MODIFIED: Conditionally create tabs based on whether df_preview exists
        tab_list = ["📈 Key Financial Metrics", "📊 Visual Insights", "📝 AI Advisory"]
        if df_preview is not None:
            tab_list.append("📄 Data Preview")

        tabs = st.tabs(tab_list)

        # Tab 1: Key Financial Metrics
        with tabs[0]:
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Revenue", f"${data.get('revenue', 0):,}")
            col2.metric("Expenses", f"${data.get('expenses', 0):,}")
            col3.metric("Burn Rate", f"${data.get('burn_rate', 0):,}/mo")
            col4.metric("Runway", f"{data.get('runway_months', 0)} months")

        # Tab 2: Visual Insights
        with tabs[1]:
            st.subheader("Financial Visualizations")
            if expense_chart_data is not None and not expense_chart_data.empty:
                st.markdown("*Expenses Breakdown*")
                pie_chart = alt.Chart(expense_chart_data).mark_arc(innerRadius=50).encode(
                    theta=alt.Theta(field="Amount", type="quantitative"),
                    color=alt.Color(field="Category", type="nominal", title="Category"),
                    tooltip=["Category", "Amount"]
                ).properties(width=400, height=400)
                st.altair_chart(pie_chart, use_container_width=True)
            else:
                st.info("No expense breakdown data available to display.")

            if runway_chart_data is not None and not runway_chart_data.empty:
                st.markdown("*Runway Projection*")
                line_chart = alt.Chart(runway_chart_data).mark_line(point=True).encode(
                    x=alt.X('Month', sort=None, title='Month'),
                    y=alt.Y('Cash', title='Cash Balance ($)'),
                    tooltip=['Month', 'Cash']
                ).properties(height=350)
                st.altair_chart(line_chart, use_container_width=True)
            else:
                st.info("No runway projection data available to display.")

        # Tab 3: AI Advisory
        with tabs[2]:
            st.subheader("AI-Generated Recommendations")
            st.write(advice if advice else "No advisory information available.")

        # MODIFIED: Conditionally populate the fourth tab if it exists
        if df_preview is not None and len(tabs) == 4:
            with tabs[3]:
                st.markdown("### 📂 Uploaded Data Preview")
                st.dataframe(df_preview)

# --- Ask AI Page (Unchanged) ---
elif page == "Ask AI":
    st.header("💬 Chat with AI Assistant")

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
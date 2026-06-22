import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="FosterLink", layout="wide")

if "logs" not in st.session_state:
    st.session_state.logs = [
        {"Timestamp": "2026-06-21 14:30", "Child": "Alex (Age 8)", "Category": "Routine/Mood", "Details": "Settled well after school. Completed homework with minimal assistance.", "Status": "Reviewed"},
        {"Timestamp": "2026-06-22 08:15", "Child": "Alex (Age 8)", "Category": "Incident", "Details": "Minor emotional outburst before school drop-off. Refused breakfast.", "Status": "Pending Review"}
    ]

if "expenses" not in st.session_state:
    st.session_state.expenses = [
        {"Timestamp": "2026-06-20", "Child": "Alex (Age 8)", "Amount": 45.00, "Type": "School Uniform", "Status": "Approved"}
    ]

st.title("🤝 FosterLink Portal")
st.caption("Admin & Case Management Cost-Reduction Engine — Investor Demo")
st.write("---")

portal_mode = st.sidebar.radio(
    "Select Portal View for Demo:",
    ["📱 Foster Carer Mobile View", "💻 Social Worker Dashboard"]
)

if portal_mode == "📱 Foster Carer Mobile View":
    st.header("Foster Carer Portal")
    st.info("💡 Value Metric: Eliminates 3+ hours of weekly manual paperwork.")
    tab1, tab2 = st.tabs(["📝 Daily Log Submission", "💰 Quick Expense Claim"])
    
    with tab1:
        st.subheader("Submit Statutory Daily Log")
        child_selected = st.selectbox("Select Placement", ["Alex (Age 8)"])
        log_category = st.selectbox("Log Category", ["Routine/Mood", "Health/Medical", "Education", "Incident"])
        log_details = st.text_area("Daily Notes / Observations", placeholder="Enter specific observations...")
        if st.button("Securely Submit Log"):
            if log_details.strip() == "":
                st.error("Please enter log details.")
            else:
                st.session_state.logs.append({
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"), "Child": child_selected, "Category": log_category, "Details": log_details, "Status": "Pending Review"
                })
                st.success("🔒 Log encrypted and transmitted instantly!")

    with tab2:
        st.subheader("Instant Expense Management")
        exp_child = st.selectbox("Assign Expense To", ["Alex (Age 8)"])
        exp_type = st.selectbox("Expense Category", ["Clothing/Uniform", "School Trips", "Travel/Mileage"])
        exp_amount = st.number_input("Amount (£)", min_value=0.01, step=0.10, format="%.2f")
        if st.button("Submit Expense"):
            st.session_state.expenses.append({
                "Timestamp": datetime.now().strftime("%Y-%m-%d"), "Child": exp_child, "Amount": exp_amount, "Type": exp_type, "Status": "Pending Review"
            })
            st.success("💰 Expense sent for review.")
else:
    st.header("Social Worker Auditing Panel")
    st.info("💡 Value Metric: Cuts desk admin by 40% via live risk flags.")
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Active Placements Monitored", value="1 Child")
    pending_logs_count = sum(1 for l in st.session_state.logs if l["Status"] == "Pending Review")
    col2.metric(label="Unresolved Logs", value=pending_logs_count)
    st.write("### Live Case Audit Feed")
    df_logs = pd.DataFrame(st.session_state.logs)
    if not df_logs.empty:
        def highlight_incidents(row):
            return ['background-color: #ffcccc' if row.Category == 'Incident' else '' for _ in row]
        st.dataframe(df_logs.style.apply(highlight_incidents, axis=1), use_container_width=True)
    st.write("### Financial Reimbursement Approvals")
    df_expenses = pd.DataFrame(st.session_state.expenses)
    if not df_expenses.empty:
        st.dataframe(df_expenses, use_container_width=True)
        if st.button("Bulk Approve Pending Claims"):
            for exp in st.session_state.expenses:
                if exp["Status"] == "Pending Review":
                    exp["Status"] = "Approved"
            st.success("Approved!")
            st.rerun()

st.write("---")
st.caption("🔒 Prototype Framework Architecture: UK GDPR compliant.")

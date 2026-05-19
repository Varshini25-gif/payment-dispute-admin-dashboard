import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

def render():
    """Render the dashboard page"""
    st.header("📊 Dashboard")
    
    # Dashboard metrics row 1
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Disputes",
            value="1,234",
            delta="+12 this week"
        )
    
    with col2:
        st.metric(
            label="Pending Disputes",
            value="456",
            delta="-8 this week"
        )
    
    with col3:
        st.metric(
            label="Resolved Disputes",
            value="678",
            delta="+20 this week"
        )
    
    with col4:
        st.metric(
            label="Resolution Rate",
            value="86.5%",
            delta="+2.3%"
        )
    
    st.markdown("---")
    
    # Data table section
    st.subheader("Recent Disputes")
    
    # Sample data
    disputes_data = {
        "Dispute ID": [f"DIS-{1000+i}" for i in range(10)],
        "Status": [random.choice(["Pending", "In Review", "Resolved"]) for _ in range(10)],
        "Amount": [f"${random.randint(100, 5000)}" for _ in range(10)],
        "Created": [(datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d") for _ in range(10)],
        "Priority": [random.choice(["Low", "Medium", "High"]) for _ in range(10)]
    }
    
    df = pd.DataFrame(disputes_data)
    
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    
    # Charts section
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Disputes by Status")
        status_data = pd.DataFrame({
            "Status": ["Pending", "In Review", "Resolved"],
            "Count": [456, 234, 678]
        })
        st.bar_chart(status_data.set_index("Status"))
    
    with col2:
        st.subheader("Disputes by Priority")
        priority_data = pd.DataFrame({
            "Priority": ["Low", "Medium", "High"],
            "Count": [300, 450, 618]
        })
        st.bar_chart(priority_data.set_index("Priority"))

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random


def generate_sample_disputes(count=10):
    """Generate sample dispute rows for placeholder tables."""
    return pd.DataFrame({
        "Dispute ID": [f"DIS-{1000 + i}" for i in range(count)],
        "Status": [random.choice(["Pending", "In Review", "Resolved"]) for _ in range(count)],
        "Amount": [f"${random.randint(100, 5000)}" for _ in range(count)],
        "Created": [(datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d") for _ in range(count)],
        "Priority": [random.choice(["Low", "Medium", "High"]) for _ in range(count)]
    })


def render_recent_disputes_table(data=None):
    """Render the recent disputes table section."""
    st.subheader("Recent Disputes")
    if data is None:
        data = generate_sample_disputes()
    st.dataframe(data, use_container_width=True, hide_index=True)

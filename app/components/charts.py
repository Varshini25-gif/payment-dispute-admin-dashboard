import streamlit as st
import pandas as pd


def render_status_chart():
    """Render a bar chart for dispute status distribution."""
    status_data = pd.DataFrame({
        "Status": ["Pending", "In Review", "Resolved"],
        "Count": [456, 234, 678]
    })
    st.subheader("Disputes by Status")
    st.bar_chart(status_data.set_index("Status"))


def render_priority_chart():
    """Render a bar chart for dispute priority distribution."""
    priority_data = pd.DataFrame({
        "Priority": ["Low", "Medium", "High"],
        "Count": [300, 450, 618]
    })
    st.subheader("Disputes by Priority")
    st.bar_chart(priority_data.set_index("Priority"))


def render_volume_chart():
    """Render an area chart showing monthly dispute volume."""
    volume_data = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Volume": [320, 410, 360, 450, 520, 480]
    })
    st.subheader("Monthly Dispute Volume")
    st.area_chart(volume_data.set_index("Month"))

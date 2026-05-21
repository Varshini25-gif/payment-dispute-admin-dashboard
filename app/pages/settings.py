import streamlit as st
from app.components.common import render_info_box


def render():
    st.header("⚙️ Settings")
    st.markdown("Configure system preferences, notification rules, and dashboard behavior.")
    render_info_box(
        "Settings Panel",
        "Settings will support integration options, alert thresholds, and account configuration."
    )
    st.markdown("---")
    st.subheader("Configuration Status")
    st.write("Placeholder settings controls are coming soon.")

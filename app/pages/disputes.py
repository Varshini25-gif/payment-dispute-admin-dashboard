import streamlit as st
from app.components.common import render_info_box


def render():
    st.header("💬 Disputes")
    st.markdown("Manage incoming disputes, review case details, and assign follow-up tasks.")
    render_info_box(
        "Disputes Workspace",
        "This page will provide dispute filtering, workflow actions, and case escalation tools. Placeholder content is shown while the full interface is built."
    )
    st.markdown("---")
    st.subheader("Dispute Queue Preview")
    st.write("Placeholder table and charts will appear here soon.")

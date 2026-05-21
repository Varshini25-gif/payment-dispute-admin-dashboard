import streamlit as st
from app.components.common import render_info_box


def render():
    st.header("👥 Users")
    st.markdown("Manage agents, reviewers, and access roles across the dispute team.")
    render_info_box(
        "User Management",
        "This page will let admins assign roles, invite new users, and audit team activity."
    )
    st.markdown("---")
    st.subheader("Team Overview")
    st.write("Placeholder user list and role controls are under development.")

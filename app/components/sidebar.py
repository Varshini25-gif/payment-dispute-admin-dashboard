import streamlit as st


def render_sidebar_navigation():
    """Create sidebar navigation and return the selected page."""
    st.sidebar.title("🏢 Admin Dashboard")
    st.sidebar.markdown("Manage dispute workflows, users, and analytics from one place.")

    page = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Disputes", "Jira Tracking", "Analytics", "SLA Monitor",
         "Routing Analytics", "Routing Rules", "Users", "Audit Logs", "Settings"],
        index=0,
        label_visibility="collapsed"
    )

    st.sidebar.markdown("---")
    st.sidebar.subheader("Quick Actions")
    st.sidebar.button("Create new case")
    st.sidebar.button("Refresh data")

    st.sidebar.markdown("---")
    st.sidebar.subheader("Info")
    st.sidebar.info(
        "Payment Dispute Admin Dashboard\n\n"
        "Version: 0.1.0\n\n"
        "Use the sidebar to switch between views and access key actions."
    )
    st.sidebar.caption("© 2026 Payment Solutions")

    return page


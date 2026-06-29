import streamlit as st


def render_sidebar_navigation():
    """Create sidebar navigation and return the selected page."""
    st.sidebar.title("Control Center")
    st.sidebar.markdown("Manage dispute workflows, users, and analytics from one place.")

    pages = [
        "Dashboard",
        "Disputes",
        "Jira Tracking",
        "Analytics",
        "SLA Monitor",
        "Routing Analytics",
        "Routing Rules",
        "Admin Controls",
        "Users",
        "Audit Logs",
        "Confluence Logs",
        "Settings",
    ]

    if "active_page" not in st.session_state:
        st.session_state["active_page"] = pages[0]

    default_index = pages.index(st.session_state["active_page"]) if st.session_state["active_page"] in pages else 0

    page = st.sidebar.radio(
        "Navigation",
        pages,
        index=default_index,
        label_visibility="collapsed"
    )
    st.session_state["active_page"] = page

    st.sidebar.markdown("---")
    st.sidebar.subheader("Quick Actions")
    st.sidebar.button("Create new case", use_container_width=True)
    st.sidebar.button("Refresh data", use_container_width=True)
    st.sidebar.caption("Tip: Use filters in each page to narrow down queue data quickly.")

    st.sidebar.markdown("---")
    st.sidebar.subheader("Workspace")
    st.sidebar.info(
        "Payment Dispute Admin Dashboard\n\n"
        "Version: 0.1.0\n\n"
        "Use the sidebar to switch between views and access key actions."
    )
    st.sidebar.caption("© 2026 Payment Solutions")

    return page


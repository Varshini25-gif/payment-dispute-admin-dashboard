import streamlit as st
from datetime import datetime


def render_top_navbar():
    """Render the top navigation bar with dashboard title and actions."""
    with st.container():
        st.markdown("<div class='pd-navbar'>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([6, 2, 2])
        with col1:
            st.markdown("<h2 class='pd-navbar-title'>Payment Dispute Admin Dashboard</h2>", unsafe_allow_html=True)
            st.markdown(
                "<p class='pd-navbar-subtitle'>Monitor dispute flow, review performance, and manage support workflows.</p>",
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown("**Current View**")
            st.caption(st.session_state.get("active_page", "Dashboard"))
            st.caption(f"Updated: {datetime.now().strftime('%d %b %Y, %H:%M')}")
        with col3:
            if st.button("Notifications", use_container_width=True):
                st.info("All systems are online. No urgent issues detected.")
            st.button("Refresh View", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


def render_page_header(title, subtitle=None):
    """Render a page section header with an optional subtitle."""
    st.markdown(f"### {title}")
    if subtitle:
        st.markdown(f"<p style='color: #6c757d;'>{subtitle}</p>", unsafe_allow_html=True)

import streamlit as st


def render_top_navbar():
    """Render the top navigation bar with dashboard title and actions."""
    with st.container():
        col1, col2, col3 = st.columns([4, 2, 1])
        with col1:
            st.markdown("## 💳 Payment Dispute Admin Dashboard")
            st.markdown("<small>Monitor dispute flow, review performance, and manage support workflows.</small>", unsafe_allow_html=True)
        with col2:
            st.markdown("**Current View**")
            st.write("Dashboard")
        with col3:
            if st.button("🔔 Notifications"):
                st.info("All systems are online. No urgent issues detected.")
            st.write("")
            st.write("")


def render_page_header(title, subtitle=None):
    """Render a page section header with an optional subtitle."""
    st.markdown(f"### {title}")
    if subtitle:
        st.markdown(f"<p style='color: #6c757d;'>{subtitle}</p>", unsafe_allow_html=True)

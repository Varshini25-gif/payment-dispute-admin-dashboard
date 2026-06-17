import os
import sys

import streamlit as st
from dotenv import load_dotenv

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.components.navbar import render_top_navbar
from app.components.sidebar import render_sidebar_navigation

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Payment Dispute Admin Dashboard",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


def render_page(page_name):
    """Render the selected page."""
    if page_name == "Dashboard":
        from app.pages.dashboard import render as render_dashboard
        render_dashboard()
    elif page_name == "Disputes":
        from app.pages.disputes import render as render_disputes
        render_disputes()
    elif page_name == "Jira Tracking":
        from app.pages.jira_tracking import render as render_jira_tracking
        render_jira_tracking()
    elif page_name == "Analytics":
        from app.pages.analytics import render as render_analytics
        render_analytics()
    elif page_name == "SLA Monitor":
        from app.pages.sla_monitor import render as render_sla_monitor
        render_sla_monitor()
    elif page_name == "Routing Analytics":
        from app.pages.routing_analytics import render as render_routing_analytics
        render_routing_analytics()
    elif page_name == "Routing Rules":
        from app.pages.routing_rules import render as render_routing_rules
        render_routing_rules()
    elif page_name == "Users":
        from app.pages.users import render as render_users
        render_users()
    elif page_name == "Audit Logs":
        from app.pages.audit_logs import render_audit_logs_page
        render_audit_logs_page()
    elif page_name == "Settings":
        from app.pages.settings import render as render_settings
        render_settings()


def main():
    """Main application entry point."""
    selected_page = render_sidebar_navigation()
    render_top_navbar()
    render_page(selected_page)


if __name__ == "__main__":
    main()

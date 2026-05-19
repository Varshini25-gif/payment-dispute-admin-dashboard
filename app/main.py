import streamlit as st
import os
from dotenv import load_dotenv

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

def sidebar_navigation():
    """Create sidebar navigation"""
    st.sidebar.title("🏢 Admin Dashboard")
    
    # Navigation menu
    page = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Disputes", "Analytics", "Users", "Settings"],
        label_visibility="collapsed"
    )
    
    # Sidebar info section
    st.sidebar.markdown("---")
    st.sidebar.subheader("ℹ️ About")
    st.sidebar.info(
        "Payment Dispute Admin Dashboard\n\n"
        "Version: 0.1.0\n\n"
        "Manage and monitor payment disputes efficiently."
    )
    
    # Sidebar footer
    st.sidebar.markdown("---")
    st.sidebar.caption("© 2024 Payment Solutions. All rights reserved.")
    
    return page

def render_page(page_name):
    """Render the selected page"""
    if page_name == "Dashboard":
        from app.pages.dashboard import render as render_dashboard
        render_dashboard()
    elif page_name == "Disputes":
        st.header("💬 Disputes Management")
        st.info("Disputes management page - Coming soon!")
    elif page_name == "Analytics":
        st.header("📊 Analytics")
        st.info("Analytics page - Coming soon!")
    elif page_name == "Users":
        st.header("👥 User Management")
        st.info("User management page - Coming soon!")
    elif page_name == "Settings":
        st.header("⚙️ Settings")
        st.info("Settings page - Coming soon!")

def main():
    """Main application entry point"""
    # Render navigation
    selected_page = sidebar_navigation()
    
    # Render selected page
    render_page(selected_page)

if __name__ == "__main__":
    main()

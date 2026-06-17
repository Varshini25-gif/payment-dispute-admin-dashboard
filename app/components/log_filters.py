"""
Log filters component
Provides filtering UI for audit logs (date range, dispute ID, action type, user).
"""

from datetime import datetime, timedelta
import streamlit as st


def render_log_filters():
    """Render filter controls for audit logs and return selected filters."""
    st.subheader("🔍 Filters")
    
    with st.form("audit_filters_form", clear_on_submit=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Date Range**")
            filter_option = st.radio(
                "Time Period",
                ["Custom", "Last 7 Days", "Last 30 Days", "Last 90 Days"],
                label_visibility="collapsed"
            )
            
            if filter_option == "Custom":
                start_date = st.date_input(
                    "Start Date",
                    value=datetime.now().date() - timedelta(days=30),
                    key="audit_start_date"
                )
                end_date = st.date_input(
                    "End Date",
                    value=datetime.now().date(),
                    key="audit_end_date"
                )
            elif filter_option == "Last 7 Days":
                end_date = datetime.now().date()
                start_date = end_date - timedelta(days=7)
            elif filter_option == "Last 30 Days":
                end_date = datetime.now().date()
                start_date = end_date - timedelta(days=30)
            else:  # Last 90 Days
                end_date = datetime.now().date()
                start_date = end_date - timedelta(days=90)
        
        with col2:
            st.markdown("**Search Filters**")
            dispute_id = st.text_input(
                "Dispute ID",
                placeholder="e.g., DIS-0001",
                key="audit_dispute_id"
            )
            action_type = st.selectbox(
                "Action Type",
                ["All", "Create", "Update", "Delete", "View", "Export", "Status Change"],
                key="audit_action_type"
            )
        
        with col3:
            st.markdown("**Additional Filters**")
            user_filter = st.text_input(
                "User/Agent",
                placeholder="Username or agent name",
                key="audit_user_filter"
            )
            severity = st.selectbox(
                "Severity",
                ["All", "Critical", "High", "Medium", "Low"],
                key="audit_severity"
            )
        
        submitted = st.form_submit_button("🔄 Apply Filters", use_container_width=True)
    
    return {
        "start_date": start_date,
        "end_date": end_date,
        "dispute_id": dispute_id if dispute_id else None,
        "action_type": action_type if action_type != "All" else None,
        "user_filter": user_filter if user_filter else None,
        "severity": severity if severity != "All" else None,
        "submitted": submitted
    }


def render_quick_filters():
    """Render quick filter buttons for common audit queries."""
    st.markdown("**Quick Filters**")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🟢 All Activity", use_container_width=True, key="quick_all"):
            return "all"
    
    with col2:
        if st.button("🚨 High Priority", use_container_width=True, key="quick_high"):
            return "high_priority"
    
    with col3:
        if st.button("⚠️ Errors Only", use_container_width=True, key="quick_errors"):
            return "errors"
    
    with col4:
        if st.button("👤 My Activities", use_container_width=True, key="quick_my"):
            return "my_activities"
    
    return None

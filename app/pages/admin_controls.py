"""
Admin Controls Page
Central hub for all administrative operations on disputes
"""

import streamlit as st
import pandas as pd

from app.components.escalation_controls import render_escalation_controls
from app.components.retry_actions import render_retry_actions
from app.components.assignment_controls import render_assignment_controls
from app.services.admin_service import admin_service


def render_dispute_override_controls():
    """Render dispute decision override controls."""
    st.subheader("⚖️ Dispute Override Controls")
    
    tab1, tab2 = st.tabs(["Override Decision", "Override History"])
    
    with tab1:
        render_override_form()
    
    with tab2:
        render_override_history()


def render_override_form():
    """Render form to override dispute decisions."""
    st.markdown("#### Override Dispute Decision")
    
    col1, col2 = st.columns(2)
    
    with col1:
        dispute_id = st.text_input(
            "Dispute ID",
            placeholder="Enter dispute ID to override",
            key="override_dispute_id"
        )
    
    with col2:
        override_decision = st.selectbox(
            "New Decision",
            ["Approved", "Rejected", "Pending Further Review", "Closed", "Escalated"],
            key="override_decision"
        )
    
    override_reason = st.text_area(
        "Override Reason (Required for audit trail)",
        placeholder="Provide detailed explanation for this decision override",
        height=120,
        key="override_reason"
    )
    
    # Additional options
    with st.expander("Advanced Options"):
        col1, col2 = st.columns(2)
        
        with col1:
            require_approval = st.checkbox(
                "Require management approval",
                value=True,
                key="require_approval"
            )
        
        with col2:
            priority_flag = st.checkbox(
                "Flag for compliance review",
                value=False,
                key="priority_flag"
            )
        
        override_notes = st.text_area(
            "Additional notes",
            placeholder="Add any additional context",
            height=80,
            key="override_notes"
        )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("⚠️ Override Decision", key="btn_override"):
            if not dispute_id:
                st.error("Please enter a Dispute ID")
            elif not override_reason:
                st.error("Please provide a reason for override")
            else:
                # Show confirmation
                st.session_state.show_override_modal = True
    
    with col2:
        if st.button("📋 View Current Status", key="btn_view_current_status"):
            if dispute_id:
                st.info("Current Status: Pending Review | Decision: Rejected | Created: 2024-01-15 10:30")
            else:
                st.error("Please enter a Dispute ID")
    
    with col3:
        if st.button("🔄 Clear Form", key="btn_clear_override"):
            st.rerun()
    
    # Confirmation handling
    from app.components.confirmation_modals import (
        confirm_override_modal, show_action_success, show_action_error
    )
    
    if confirm_override_modal():
        try:
            response = admin_service.override_dispute_decision(
                dispute_id=dispute_id,
                override_decision=override_decision,
                override_reason=override_reason
            )
            
            show_action_success(
                "Dispute Override",
                f"Dispute {dispute_id} decision has been overridden to {override_decision}"
            )
            
            # Clear form
            st.session_state.override_dispute_id = ""
            st.session_state.override_reason = ""
            
        except Exception as e:
            show_action_error("Dispute Override", str(e))


def render_override_history():
    """Render override decision history."""
    st.markdown("#### Override History")
    
    col1, col2 = st.columns(2)
    
    with col1:
        days_back = st.slider(
            "Days to look back",
            1, 90, 7,
            key="override_history_days"
        )
    
    with col2:
        override_decision_filter = st.selectbox(
            "Filter by Decision",
            ["All", "Approved", "Rejected", "Pending Further Review", "Closed", "Escalated"],
            key="override_decision_filter"
        )
    
    st.markdown("---")
    
    # Override statistics
    st.write("**Override Statistics (7 days)**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Overrides", 12)
        st.metric("Approvals", 8)
    
    with col2:
        st.metric("Rejections", 2)
        st.metric("Pending Review", 2)
    
    with col3:
        st.metric("Avg Review Time", "3.2h")
        st.metric("Override Rate", "2.4%")
    
    st.markdown("---")
    
    # Override history table
    st.write("**Recent Overrides**")
    
    history_data = {
        "Date": ["2024-01-15 14:30", "2024-01-15 12:15", "2024-01-15 10:45", "2024-01-14 16:20", "2024-01-14 13:30"],
        "Dispute ID": ["D001", "D002", "D003", "D004", "D005"],
        "Original Decision": ["Rejected", "Rejected", "Approved", "Rejected", "Pending"],
        "Override Decision": ["Approved", "Pending Review", "Rejected", "Escalated", "Closed"],
        "Admin": ["John Smith", "Jane Doe", "John Smith", "Mike Johnson", "Jane Doe"],
        "Reason": ["Customer Appeal", "Documentation Error", "Policy Exception", "SLA Risk", "Compliance Issue"],
        "Status": ["Completed", "In Review", "Completed", "Approved", "Completed"]
    }
    
    history_df = pd.DataFrame(history_data)
    st.dataframe(history_df, use_container_width=True, hide_index=True)


def render_quick_actions():
    """Render quick actions panel."""
    st.markdown("## ⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📤 Escalate Dispute", key="quick_escalate", use_container_width=True):
            st.session_state.active_section = "Escalation Management"
            st.rerun()
    
    with col2:
        if st.button("🔄 Retry Processing", key="quick_retry", use_container_width=True):
            st.session_state.active_section = "Retry & Reprocessing"
            st.rerun()
    
    with col3:
        if st.button("👥 Assign Dispute", key="quick_assign", use_container_width=True):
            st.session_state.active_section = "Queue & Assignment Management"
            st.rerun()
    
    with col4:
        if st.button("⚖️ Override Decision", key="quick_override", use_container_width=True):
            st.session_state.active_section = "Dispute Override Controls"
            st.rerun()


def render_admin_dashboard():
    """Render main admin dashboard with key metrics."""
    st.markdown("## 📊 Admin Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Escalations (24h)", 12, "↑ 2")
    
    with col2:
        st.metric("Pending Retries", 8, "↓ 1")
    
    with col3:
        st.metric("Manual Assignments", 34, "normal")
    
    with col4:
        st.metric("Decision Overrides", 5, "↓ 2")
    
    st.markdown("---")
    
    # Recent admin activities
    st.markdown("## 📋 Recent Admin Activities")
    
    activities = {
        "Time": ["14:30", "13:45", "13:15", "12:30", "11:50"],
        "Action": ["Escalation", "Override", "Retry", "Assignment", "Escalation"],
        "Dispute ID": ["D123", "D124", "D125", "D126", "D127"],
        "Admin": ["John Smith", "Jane Doe", "John Smith", "Mike Johnson", "Jane Doe"],
        "Status": ["✅ Success", "✅ Success", "⏳ In Progress", "✅ Success", "✅ Success"]
    }
    
    activities_df = pd.DataFrame(activities)
    st.dataframe(activities_df, use_container_width=True, hide_index=True)


def render():
    """Main render function for the admin controls page."""
    st.title("💼 Admin Controls Center")
    
    st.write("Manage all administrative operations for dispute resolution including escalations, retries, assignments, and overrides.")
    
    st.markdown("---")
    
    # Quick actions
    render_quick_actions()
    
    st.markdown("---")
    
    # Admin dashboard
    render_admin_dashboard()
    
    st.markdown("---")
    
    # Main sections in tabs
    main_tab1, main_tab2, main_tab3, main_tab4, main_tab5 = st.tabs([
        "🚨 Escalations",
        "🔄 Retries",
        "👥 Assignments",
        "⚖️ Overrides",
        "📊 Analytics"
    ])
    
    with main_tab1:
        render_escalation_controls()
    
    with main_tab2:
        render_retry_actions()
    
    with main_tab3:
        render_assignment_controls()
    
    with main_tab4:
        render_dispute_override_controls()
    
    with main_tab5:
        render_admin_analytics()


def render_admin_analytics():
    """Render admin analytics and reporting."""
    st.subheader("📊 Admin Operations Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        metric_type = st.selectbox(
            "Select Metric",
            ["Escalations", "Retries", "Assignments", "Overrides", "All Operations"],
            key="analytics_metric"
        )
    
    with col2:
        time_period = st.selectbox(
            "Time Period",
            ["Last 7 days", "Last 30 days", "Last 90 days", "YTD"],
            key="analytics_period"
        )
    
    st.markdown("---")
    
    # Summary stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Operations", 247, "↑ 18%")
    
    with col2:
        st.metric("Avg Resolution Time", "4.2h", "↓ 0.3h")
    
    with col3:
        st.metric("Success Rate", "94.2%", "↑ 2%")
    
    st.markdown("---")
    
    # Operations breakdown
    st.write("**Operations by Type**")
    
    breakdown_data = {
        "Operation": ["Escalations", "Retries", "Assignments", "Overrides"],
        "Count": [42, 85, 92, 28],
        "Success Rate": ["95.2%", "91.8%", "98.9%", "89.3%"],
        "Avg Time": ["3.2h", "2.1h", "0.8h", "5.4h"]
    }
    
    breakdown_df = pd.DataFrame(breakdown_data)
    st.dataframe(breakdown_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Top admins by activity
    st.write("**Top Admins by Activity**")
    
    admin_data = {
        "Admin Name": ["John Smith", "Jane Doe", "Mike Johnson", "Sarah Williams"],
        "Operations": [56, 48, 32, 28],
        "Escalations": [12, 15, 8, 7],
        "Retries": [20, 18, 10, 8],
        "Assignments": [18, 12, 12, 10],
        "Overrides": [6, 3, 2, 3]
    }
    
    admin_df = pd.DataFrame(admin_data)
    st.dataframe(admin_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Trends
    st.write("**Operational Trends**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("📈 Escalations increased by 15% over last week - May indicate operational challenges")
    
    with col2:
        st.info("✅ Override success rate at 89% - Above target of 85%")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.warning("⚠️ Retry operations pending review for 5+ disputes")
    
    with col2:
        st.success("✅ Assignment completion time decreased to 0.8h average")


if __name__ == "__main__":
    render()

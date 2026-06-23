"""
Retry Actions Component
Handles dispute retry and reprocessing functionality
"""

import streamlit as st
import pandas as pd

from app.services.admin_service import admin_service
from app.components.confirmation_modals import (
    confirm_retry_modal, show_action_success, show_action_error
)


def render_retry_actions():
    """Render the retry actions interface."""
    st.subheader("🔄 Retry & Reprocessing")
    
    # Tabs for different retry views
    tab1, tab2, tab3 = st.tabs([
        "Retry Dispute",
        "Pending Retries",
        "Retry History"
    ])
    
    with tab1:
        render_retry_dispute_form()
    
    with tab2:
        render_pending_retries()
    
    with tab3:
        render_retry_history()


def render_retry_dispute_form():
    """Render form to retry a dispute."""
    st.markdown("#### Retry Dispute Processing")
    
    col1, col2 = st.columns(2)
    
    with col1:
        dispute_id = st.text_input(
            "Dispute ID",
            placeholder="Enter dispute ID to retry",
            key="retry_dispute_id"
        )
    
    with col2:
        retry_type = st.selectbox(
            "Retry Type",
            ["Full Reprocessing", "API Integration", "Document Verification", "Payment Verification", "Custom"],
            key="retry_type"
        )
    
    retry_reason = st.text_area(
        "Reason for Retry",
        placeholder="Explain why this dispute needs to be reprocessed",
        height=100,
        key="retry_reason"
    )
    
    # Additional options
    with st.expander("Advanced Options"):
        skip_previous = st.checkbox(
            "Skip previous failed steps",
            value=False,
            key="skip_previous_steps"
        )
        priority_boost = st.checkbox(
            "Boost priority in queue",
            value=False,
            key="priority_boost"
        )
        notify_assignee = st.checkbox(
            "Notify assigned agent",
            value=True,
            key="notify_assignee"
        )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Retry Dispute", key="btn_retry_dispute"):
            if not dispute_id:
                st.error("Please enter a Dispute ID")
            elif not retry_reason:
                st.error("Please provide a reason for retry")
            else:
                st.session_state.show_retry_modal = True
    
    with col2:
        if st.button("🔍 View Details", key="btn_view_retry_details"):
            if dispute_id:
                st.session_state.selected_dispute_retry = dispute_id
            else:
                st.error("Please enter a Dispute ID")
    
    with col3:
        if st.button("🔄 Clear Form", key="btn_clear_retry"):
            st.rerun()
    
    # Confirmation modal
    if confirm_retry_modal():
        try:
            response = admin_service.retry_dispute_processing(
                dispute_id=dispute_id,
                retry_reason=retry_reason
            )
            
            show_action_success(
                "Dispute Retry",
                f"Dispute {dispute_id} has been queued for reprocessing"
            )
            
            # Clear form
            st.session_state.retry_dispute_id = ""
            st.session_state.retry_reason = ""
            
        except Exception as e:
            show_action_error("Dispute Retry", str(e))


def render_pending_retries():
    """Render list of pending retries."""
    st.markdown("#### Pending Retries")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_type = st.selectbox(
            "Filter by Type",
            ["All", "Full Reprocessing", "API Integration", "Document Verification", "Payment Verification"],
            key="retry_filter_type"
        )
    
    with col2:
        filter_status = st.selectbox(
            "Filter by Status",
            ["All", "Pending", "In Progress", "Completed", "Failed"],
            key="retry_filter_status"
        )
    
    with col3:
        sort_by = st.selectbox(
            "Sort by",
            ["Newest", "Oldest", "Priority"],
            key="retry_sort"
        )
    
    st.markdown("---")
    
    # Mock pending retries data
    pending_retries = [
        {
            "Retry ID": "R001",
            "Dispute ID": "D123",
            "Type": "API Integration",
            "Status": "In Progress",
            "Created": "2024-01-15 10:30",
            "Attempts": 1,
            "Next Retry": "2024-01-15 15:30"
        },
        {
            "Retry ID": "R002",
            "Dispute ID": "D124",
            "Type": "Document Verification",
            "Status": "Pending",
            "Created": "2024-01-15 09:15",
            "Attempts": 0,
            "Next Retry": "2024-01-15 11:15"
        },
        {
            "Retry ID": "R003",
            "Dispute ID": "D125",
            "Type": "Payment Verification",
            "Status": "Pending",
            "Created": "2024-01-15 08:00",
            "Attempts": 0,
            "Next Retry": "2024-01-15 10:00"
        }
    ]
    
    retries_df = pd.DataFrame(pending_retries)
    st.dataframe(retries_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.markdown("##### Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_retry = st.selectbox(
            "Select retry to manage",
            [r["Retry ID"] for r in pending_retries],
            key="selected_retry_manage"
        )
    
    with col2:
        if st.button("⏱️ Retry Now", key="btn_retry_now"):
            if selected_retry:
                try:
                    st.success(f"✅ Retry {selected_retry} has been triggered immediately")
                except Exception as e:
                    show_action_error("Immediate Retry", str(e))
    
    with col3:
        if st.button("❌ Cancel Retry", key="btn_cancel_retry"):
            if selected_retry:
                try:
                    # Extract retry_id from selection
                    response = admin_service.cancel_retry(retry_id=selected_retry)
                    show_action_success("Cancel Retry", f"Retry {selected_retry} has been cancelled")
                except Exception as e:
                    show_action_error("Cancel Retry", str(e))
    
    # Retry details
    if selected_retry:
        st.markdown("---")
        st.markdown(f"**Details for {selected_retry}**")
        
        # Find the selected retry
        selected_data = next((r for r in pending_retries if r["Retry ID"] == selected_retry), None)
        if selected_data:
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Dispute ID:** {selected_data['Dispute ID']}")
                st.write(f"**Type:** {selected_data['Type']}")
                st.write(f"**Status:** {selected_data['Status']}")
            with col2:
                st.write(f"**Created:** {selected_data['Created']}")
                st.write(f"**Attempts:** {selected_data['Attempts']}")
                st.write(f"**Next Retry:** {selected_data['Next Retry']}")


def render_retry_history():
    """Render retry history and statistics."""
    st.markdown("#### Retry History & Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        days_back = st.slider(
            "Days to look back",
            1, 90, 7,
            key="retry_history_days"
        )
    
    with col2:
        retry_type_filter = st.selectbox(
            "Filter by Type",
            ["All", "Full Reprocessing", "API Integration", "Document Verification", "Payment Verification"],
            key="history_type_filter"
        )
    
    st.markdown("---")
    st.write("**Retry Statistics**")
    
    # Mock retry statistics
    retry_stats = {
        "Total Retries (7d)": 47,
        "Successful": 38,
        "Failed": 5,
        "Pending": 4,
        "Success Rate": "80.9%",
        "Avg Attempts": 1.8
    }
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Retries", retry_stats["Total Retries (7d)"])
        st.metric("Successful", retry_stats["Successful"], "✅")
    
    with col2:
        st.metric("Failed", retry_stats["Failed"], "❌")
        st.metric("Pending", retry_stats["Pending"], "⏳")
    
    with col3:
        st.metric("Success Rate", retry_stats["Success Rate"])
        st.metric("Avg Attempts", retry_stats["Avg Attempts"])
    
    st.markdown("---")
    
    # Retry history by type
    st.write("**Retries by Type**")
    
    type_stats = {
        "Full Reprocessing": 18,
        "API Integration": 12,
        "Document Verification": 10,
        "Payment Verification": 7
    }
    
    type_df = pd.DataFrame([
        {"Type": k, "Count": v, "Success Rate": "85%"} 
        for k, v in type_stats.items()
    ])
    
    st.dataframe(type_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Recent retry history
    st.write("**Recent Retries**")
    
    history_data = {
        "Dispute ID": ["D001", "D002", "D003", "D004", "D005"],
        "Type": ["API Integration", "Document", "Payment", "Full", "API Integration"],
        "Result": ["✅ Success", "✅ Success", "❌ Failed", "✅ Success", "⏳ Pending"],
        "Attempts": [1, 2, 3, 1, 2],
        "Date": ["2024-01-15 14:30", "2024-01-15 12:45", "2024-01-15 11:20", "2024-01-14 16:00", "2024-01-14 13:30"]
    }
    
    history_df = pd.DataFrame(history_data)
    st.dataframe(history_df, use_container_width=True, hide_index=True)

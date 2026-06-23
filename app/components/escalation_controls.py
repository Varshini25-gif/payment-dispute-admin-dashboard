"""
Escalation Controls Component
Handles dispute escalation functionality
"""

import streamlit as st
import pandas as pd

from app.services.admin_service import admin_service
from app.components.confirmation_modals import (
    confirm_escalation_modal, show_action_success, show_action_error
)
from app.components.common import render_status_badge, render_priority_badge


def render_escalation_controls():
    """Render the escalation controls interface."""
    st.subheader("🚨 Escalation Management")
    
    # Tabs for different escalation views
    tab1, tab2, tab3 = st.tabs([
        "Escalate Dispute",
        "Active Escalations",
        "Escalation History"
    ])
    
    with tab1:
        render_escalate_dispute_form()
    
    with tab2:
        render_active_escalations()
    
    with tab3:
        render_escalation_history()


def render_escalate_dispute_form():
    """Render form to escalate a dispute."""
    st.markdown("#### Escalate a Dispute")
    
    col1, col2 = st.columns(2)
    
    with col1:
        dispute_id = st.text_input(
            "Dispute ID",
            placeholder="Enter dispute ID to escalate",
            key="escalate_dispute_id"
        )
    
    with col2:
        escalation_level = st.selectbox(
            "Escalation Level",
            ["Level 1 - Supervisor Review", "Level 2 - Manager Review", "Level 3 - Executive Review"],
            key="escalation_level"
        )
    
    escalation_reason = st.text_area(
        "Reason for Escalation",
        placeholder="Explain why this dispute needs escalation",
        height=100,
        key="escalation_reason"
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📤 Escalate Dispute", key="btn_escalate"):
            if not dispute_id:
                st.error("Please enter a Dispute ID")
            elif not escalation_reason:
                st.error("Please provide a reason for escalation")
            else:
                st.session_state.show_escalation_modal = True
    
    with col2:
        if st.button("🔍 Search Dispute", key="btn_search_dispute"):
            if dispute_id:
                st.session_state.search_dispute_id = dispute_id
            else:
                st.error("Please enter a Dispute ID")
    
    with col3:
        if st.button("🔄 Clear Form", key="btn_clear_escalate"):
            st.rerun()
    
    # Confirmation modal
    if confirm_escalation_modal():
        try:
            # Extract level number from selection
            level_map = {
                "Level 1 - Supervisor Review": 1,
                "Level 2 - Manager Review": 2,
                "Level 3 - Executive Review": 3
            }
            level_num = level_map.get(escalation_level, 1)
            
            response = admin_service.escalate_dispute(
                dispute_id=dispute_id,
                escalation_reason=escalation_reason,
                escalation_level=level_num
            )
            
            show_action_success(
                "Escalation",
                f"Dispute {dispute_id} has been escalated to {escalation_level}"
            )
            
            # Clear form
            st.session_state.escalate_dispute_id = ""
            st.session_state.escalation_reason = ""
            
        except Exception as e:
            show_action_error("Escalation", str(e))


def render_active_escalations():
    """Render list of active escalations."""
    st.markdown("#### Active Escalations")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_level = st.selectbox(
            "Filter by Level",
            ["All", "Level 1", "Level 2", "Level 3"],
            key="escalation_filter_level"
        )
    
    with col2:
        filter_status = st.selectbox(
            "Filter by Status",
            ["All", "Pending", "In Review", "Resolved"],
            key="escalation_filter_status"
        )
    
    with col3:
        sort_by = st.selectbox(
            "Sort by",
            ["Newest", "Oldest", "Priority"],
            key="escalation_sort"
        )
    
    # Load escalations
    try:
        status_param = None if filter_status == "All" else filter_status.lower()
        escalations_data = admin_service.get_escalations(status=status_param, limit=50)
        
        if escalations_data and "data" in escalations_data:
            escalations = escalations_data["data"]
            
            if escalations:
                # Display escalations as a table
                escalation_df = pd.DataFrame(escalations)
                
                # Select columns for display
                display_cols = []
                if "dispute_id" in escalation_df.columns:
                    display_cols.append("dispute_id")
                if "customer_name" in escalation_df.columns:
                    display_cols.append("customer_name")
                if "escalation_level" in escalation_df.columns:
                    display_cols.append("escalation_level")
                if "status" in escalation_df.columns:
                    display_cols.append("status")
                if "created_date" in escalation_df.columns:
                    display_cols.append("created_date")
                
                display_cols = [c for c in display_cols if c in escalation_df.columns]
                
                st.dataframe(
                    escalation_df[display_cols] if display_cols else escalation_df,
                    use_container_width=True,
                    hide_index=True
                )
                
                # Individual escalation actions
                st.markdown("##### Actions")
                selected_escalation_id = st.selectbox(
                    "Select escalation to manage",
                    escalations[0].get("id", "Select...") if escalations else ["No escalations"],
                    key="selected_escalation_manage"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Mark as Resolved", key="btn_resolve_escalation"):
                        try:
                            response = admin_service.resolve_escalation(
                                escalation_id=selected_escalation_id,
                                resolution="Manually resolved by admin"
                            )
                            show_action_success("Escalation Resolution", "Escalation marked as resolved")
                        except Exception as e:
                            show_action_error("Escalation Resolution", str(e))
                
                with col2:
                    if st.button("📝 Add Note", key="btn_add_escalation_note"):
                        st.text_area("Add a note to this escalation:", key="escalation_note")
            else:
                st.info("No active escalations found")
        else:
            st.info("No escalations data available")
    
    except Exception as e:
        st.error(f"Failed to load escalations: {str(e)}")


def render_escalation_history():
    """Render escalation history and statistics."""
    st.markdown("#### Escalation History")
    
    col1, col2 = st.columns(2)
    
    with col1:
        days_back = st.slider(
            "Days to look back",
            1, 90, 7,
            key="escalation_history_days"
        )
    
    with col2:
        sort_history = st.selectbox(
            "Sort by",
            ["Most Recent", "Most Frequent", "Highest Level"],
            key="history_sort"
        )
    
    st.markdown("---")
    st.write("**Escalation Trends**")
    
    # Mock data for escalation trends
    escalation_stats = {
        "Total Escalations (7 days)": 24,
        "Level 1 Escalations": 16,
        "Level 2 Escalations": 6,
        "Level 3 Escalations": 2,
        "Average Resolution Time": "4.2 hours",
        "Most Common Reason": "SLA Risk"
    }
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Escalations (7d)", escalation_stats["Total Escalations (7 days)"])
        st.metric("Level 1", escalation_stats["Level 1 Escalations"])
    
    with col2:
        st.metric("Level 2", escalation_stats["Level 2 Escalations"])
        st.metric("Level 3", escalation_stats["Level 3 Escalations"])
    
    with col3:
        st.metric("Avg. Resolution", escalation_stats["Average Resolution Time"])
        st.metric("Top Reason", escalation_stats["Most Common Reason"])
    
    st.markdown("---")
    
    # Recent escalation history table
    st.write("**Recent Escalations**")
    history_data = {
        "Dispute ID": ["D001", "D002", "D003", "D004", "D005"],
        "Level": [1, 2, 1, 3, 1],
        "Reason": ["SLA Risk", "Complex Case", "Customer Complaint", "Fraud Review", "Documentation"],
        "Created": ["2024-01-15 10:30", "2024-01-15 09:15", "2024-01-14 16:45", "2024-01-14 14:20", "2024-01-13 11:00"],
        "Status": ["Resolved", "In Review", "Resolved", "Pending", "Resolved"]
    }
    
    history_df = pd.DataFrame(history_data)
    st.dataframe(history_df, use_container_width=True, hide_index=True)

"""
Assignment Controls Component
Handles manual dispute assignment to queues and agents
"""

import streamlit as st
import pandas as pd

from app.services.admin_service import admin_service
from app.components.confirmation_modals import (
    confirm_assignment_modal, show_action_success, show_action_error
)


def render_assignment_controls():
    """Render the assignment controls interface."""
    st.subheader("👥 Queue & Assignment Management")
    
    # Tabs for different assignment views
    tab1, tab2, tab3 = st.tabs([
        "Manual Assignment",
        "Queue Status",
        "Assignment History"
    ])
    
    with tab1:
        render_manual_assignment_form()
    
    with tab2:
        render_queue_status()
    
    with tab3:
        render_assignment_history()


def render_manual_assignment_form():
    """Render form to manually assign disputes."""
    st.markdown("#### Manual Dispute Assignment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        dispute_id = st.text_input(
            "Dispute ID",
            placeholder="Enter dispute ID to assign",
            key="assign_dispute_id"
        )
    
    with col2:
        assignment_type = st.selectbox(
            "Assignment Type",
            ["Assign to Agent", "Assign to Queue", "Reassign"],
            key="assignment_type"
        )
    
    # Load available agents and queues
    try:
        agents_data = admin_service.get_available_agents()
        
        if agents_data and "data" in agents_data:
            agents = agents_data["data"]
            agent_list = [f"{a.get('name', '')} ({a.get('agent_id', '')})" for a in agents]
        else:
            agent_list = ["Agent 1 (A001)", "Agent 2 (A002)", "Agent 3 (A003)", "Agent 4 (A004)"]
    except:
        agent_list = ["Agent 1 (A001)", "Agent 2 (A002)", "Agent 3 (A003)", "Agent 4 (A004)"]
    
    # Queue options
    queue_list = [
        "General Queue",
        "High Priority Queue",
        "SLA Risk Queue",
        "Escalation Queue",
        "Complex Cases Queue"
    ]
    
    if assignment_type == "Assign to Agent":
        selected_agent = st.selectbox(
            "Select Agent",
            agent_list,
            key="selected_agent"
        )
        agent_display = selected_agent
    elif assignment_type == "Assign to Queue":
        selected_queue = st.selectbox(
            "Select Queue",
            queue_list,
            key="selected_queue"
        )
        agent_display = selected_queue
    else:  # Reassign
        selected_agent = st.selectbox(
            "Reassign to Agent",
            agent_list,
            key="reassign_agent"
        )
        agent_display = selected_agent
    
    # Assignment notes
    assignment_notes = st.text_area(
        "Assignment Notes",
        placeholder="Add notes about this assignment (optional)",
        height=80,
        key="assignment_notes"
    )
    
    # Assignment priority
    col1, col2 = st.columns(2)
    with col1:
        priority = st.selectbox(
            "Priority",
            ["Normal", "High", "Low"],
            key="assignment_priority"
        )
    
    with col2:
        send_notification = st.checkbox(
            "Send notification to agent",
            value=True,
            key="send_notification"
        )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("👤 Assign Now", key="btn_assign"):
            if not dispute_id:
                st.error("Please enter a Dispute ID")
            else:
                st.session_state.show_assignment_modal = True
    
    with col2:
        if st.button("🔍 Check Availability", key="btn_check_availability"):
            render_agent_availability()
    
    with col3:
        if st.button("🔄 Clear Form", key="btn_clear_assign"):
            st.rerun()
    
    # Confirmation modal
    if confirm_assignment_modal(agent_info=agent_display):
        try:
            if assignment_type == "Assign to Agent":
                # Extract agent ID from agent_display
                agent_id = agent_display.split("(")[1].rstrip(")")
            else:
                # Queue assignment
                agent_id = selected_queue
            
            response = admin_service.assign_dispute(
                dispute_id=dispute_id,
                assignee_id=agent_id,
                queue=selected_queue if assignment_type == "Assign to Queue" else None
            )
            
            show_action_success(
                "Assignment",
                f"Dispute {dispute_id} has been assigned to {agent_display}"
            )
            
            # Clear form
            st.session_state.assign_dispute_id = ""
            st.session_state.assignment_notes = ""
            
        except Exception as e:
            show_action_error("Assignment", str(e))


def render_agent_availability():
    """Render agent availability information."""
    st.markdown("---")
    st.markdown("##### Agent Availability")
    
    availability_data = {
        "Agent ID": ["A001", "A002", "A003", "A004", "A005"],
        "Name": ["Alice Johnson", "Bob Smith", "Carol Davis", "David Wilson", "Emma Brown"],
        "Status": ["Available", "Busy", "Available", "On Break", "Available"],
        "Current Load": ["3/5", "5/5", "2/5", "-", "4/5"],
        "Avg Handle Time": ["2.1h", "2.5h", "1.9h", "-", "2.3h"],
        "Queue": ["General", "Escalation", "General", "-", "High Priority"]
    }
    
    availability_df = pd.DataFrame(availability_data)
    st.dataframe(availability_df, use_container_width=True, hide_index=True)
    st.markdown("---")


def render_queue_status():
    """Render current queue status and analytics."""
    st.markdown("#### Queue Status & Analytics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        queue_filter = st.selectbox(
            "Select Queue",
            ["All Queues", "General Queue", "High Priority Queue", "SLA Risk Queue", "Escalation Queue", "Complex Cases Queue"],
            key="queue_filter"
        )
    
    with col2:
        time_range = st.selectbox(
            "Time Range",
            ["Last Hour", "Last 4 Hours", "Today", "This Week"],
            key="queue_time_range"
        )
    
    with col3:
        if st.button("🔄 Refresh Data", key="btn_refresh_queue"):
            st.rerun()
    
    st.markdown("---")
    
    # Queue metrics
    st.write("**Queue Metrics**")
    
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    
    with metrics_col1:
        st.metric("Total Cases in Queue", "127", "↑ 12 today")
    
    with metrics_col2:
        st.metric("Avg Wait Time", "23 min", "↓ 5 min")
    
    with metrics_col3:
        st.metric("Cases Over SLA", "8", "⚠️")
    
    with metrics_col4:
        st.metric("Queue Health", "85%", "✅")
    
    st.markdown("---")
    
    # Queue breakdown
    st.write("**Queue Breakdown**")
    
    queue_data = {
        "Queue": ["General Queue", "High Priority Queue", "SLA Risk Queue", "Escalation Queue", "Complex Cases Queue"],
        "Cases": [45, 28, 18, 22, 14],
        "Avg Wait": ["15 min", "8 min", "35 min", "12 min", "42 min"],
        "Over SLA": [1, 0, 4, 2, 1],
        "Assigned Agents": [5, 3, 2, 4, 2]
    }
    
    queue_df = pd.DataFrame(queue_data)
    st.dataframe(queue_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Load balancing suggestions
    st.write("**Load Balancing Suggestions**")
    
    suggestions = [
        "⚠️ SLA Risk Queue has 4 cases over SLA - Consider reassigning to available agents",
        "✅ General Queue is operating normally",
        "💡 High Priority Queue is well-staffed - Can absorb additional cases if needed",
        "⏱️ Complex Cases Queue has high average wait time - May need additional resources"
    ]
    
    for suggestion in suggestions:
        st.info(suggestion)


def render_assignment_history():
    """Render assignment history and patterns."""
    st.markdown("#### Assignment History & Patterns")
    
    col1, col2 = st.columns(2)
    
    with col1:
        days_back = st.slider(
            "Days to look back",
            1, 90, 7,
            key="assignment_history_days"
        )
    
    with col2:
        agent_filter = st.selectbox(
            "Filter by Agent",
            ["All Agents", "Alice Johnson", "Bob Smith", "Carol Davis", "David Wilson", "Emma Brown"],
            key="assignment_agent_filter"
        )
    
    st.markdown("---")
    
    # Assignment statistics
    st.write("**Assignment Statistics (7 days)**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Assignments", 156)
        st.metric("Manual Assignments", 34)
    
    with col2:
        st.metric("Avg Assignments/Agent", 26)
        st.metric("Reassignments", 8)
    
    with col3:
        st.metric("Auto vs Manual", "78% vs 22%")
        st.metric("Successful Assignments", "98%")
    
    st.markdown("---")
    
    # Recent assignments
    st.write("**Recent Assignments**")
    
    history_data = {
        "Date": ["2024-01-15 14:30", "2024-01-15 13:15", "2024-01-15 12:00", "2024-01-15 10:45", "2024-01-15 09:30"],
        "Dispute ID": ["D001", "D002", "D003", "D004", "D005"],
        "Assigned To": ["Alice Johnson", "Bob Smith", "Carol Davis", "Emma Brown", "Alice Johnson"],
        "Queue": ["General", "Escalation", "High Priority", "General", "Complex Cases"],
        "Type": ["Manual", "Auto", "Manual", "Auto", "Manual"],
        "Status": ["Accepted", "Accepted", "In Progress", "Completed", "Accepted"]
    }
    
    history_df = pd.DataFrame(history_data)
    st.dataframe(history_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Agent performance
    st.write("**Agent Performance**")
    
    agent_perf = {
        "Agent": ["Alice Johnson", "Bob Smith", "Carol Davis", "David Wilson", "Emma Brown"],
        "Assignments": [28, 24, 22, 26, 25],
        "Avg Resolution Time": ["2.1h", "2.5h", "1.9h", "2.4h", "2.2h"],
        "CSAT Score": ["4.8/5", "4.6/5", "4.9/5", "4.7/5", "4.8/5"],
        "Utilization": ["92%", "88%", "95%", "85%", "90%"]
    }
    
    perf_df = pd.DataFrame(agent_perf)
    st.dataframe(perf_df, use_container_width=True, hide_index=True)

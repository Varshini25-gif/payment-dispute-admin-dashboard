"""
Confirmation Modals Component
Reusable confirmation dialogs for admin actions
"""

import streamlit as st


def confirm_escalation_modal():
    """Modal for confirming dispute escalation."""
    if "show_escalation_modal" not in st.session_state:
        st.session_state.show_escalation_modal = False

    if st.session_state.show_escalation_modal:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("---")
            st.warning("⚠️ **Confirm Escalation**")
            st.write("You are about to escalate this dispute. This action will:")
            st.write("• Move the case to a higher priority queue")
            st.write("• Notify assigned stakeholders")
            st.write("• Create an audit trail entry")
            
            col_confirm, col_cancel = st.columns(2)
            with col_confirm:
                if st.button("✅ Confirm Escalation", key="confirm_escalation"):
                    st.session_state.show_escalation_modal = False
                    return True
            with col_cancel:
                if st.button("❌ Cancel", key="cancel_escalation"):
                    st.session_state.show_escalation_modal = False
                    return False
            st.markdown("---")
    
    return None


def confirm_retry_modal():
    """Modal for confirming dispute retry."""
    if "show_retry_modal" not in st.session_state:
        st.session_state.show_retry_modal = False

    if st.session_state.show_retry_modal:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("---")
            st.warning("⚠️ **Confirm Retry**")
            st.write("You are about to retry processing this dispute. This action will:")
            st.write("• Restart the dispute processing workflow")
            st.write("• Clear any error states")
            st.write("• Create an audit trail entry")
            
            col_confirm, col_cancel = st.columns(2)
            with col_confirm:
                if st.button("✅ Confirm Retry", key="confirm_retry"):
                    st.session_state.show_retry_modal = False
                    return True
            with col_cancel:
                if st.button("❌ Cancel", key="cancel_retry"):
                    st.session_state.show_retry_modal = False
                    return False
            st.markdown("---")
    
    return None


def confirm_assignment_modal(agent_info=None):
    """Modal for confirming manual assignment."""
    if "show_assignment_modal" not in st.session_state:
        st.session_state.show_assignment_modal = False

    if st.session_state.show_assignment_modal:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("---")
            st.warning("⚠️ **Confirm Assignment**")
            st.write("You are about to manually assign this dispute. This action will:")
            st.write("• Unassign the current owner (if any)")
            if agent_info:
                st.write(f"• Assign to: **{agent_info}**")
            st.write("• Update dispute status to 'Assigned'")
            st.write("• Create an audit trail entry")
            
            col_confirm, col_cancel = st.columns(2)
            with col_confirm:
                if st.button("✅ Confirm Assignment", key="confirm_assignment"):
                    st.session_state.show_assignment_modal = False
                    return True
            with col_cancel:
                if st.button("❌ Cancel", key="cancel_assignment"):
                    st.session_state.show_assignment_modal = False
                    return False
            st.markdown("---")
    
    return None


def confirm_override_modal(current_status=None, new_status=None):
    """Modal for confirming dispute decision override."""
    if "show_override_modal" not in st.session_state:
        st.session_state.show_override_modal = False

    if st.session_state.show_override_modal:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("---")
            st.error("🛑 **Confirm Override - Critical Action**")
            st.write("You are about to override the dispute decision. This action will:")
            if current_status and new_status:
                st.write(f"• Change status from **{current_status}** to **{new_status}**")
            st.write("• Override all automated decisions")
            st.write("• Require management review")
            st.write("• Create a detailed audit trail entry")
            
            st.write("This is a critical admin action. Proceed with caution.")
            
            col_confirm, col_cancel = st.columns(2)
            with col_confirm:
                if st.button("✅ Confirm Override", key="confirm_override"):
                    st.session_state.show_override_modal = False
                    return True
            with col_cancel:
                if st.button("❌ Cancel", key="cancel_override"):
                    st.session_state.show_override_modal = False
                    return False
            st.markdown("---")
    
    return None


def confirm_bulk_action_modal(action_name, dispute_count):
    """Modal for confirming bulk admin actions."""
    if "show_bulk_action_modal" not in st.session_state:
        st.session_state.show_bulk_action_modal = False

    if st.session_state.show_bulk_action_modal:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("---")
            st.warning(f"⚠️ **Confirm Bulk Action: {action_name}**")
            st.write(f"You are about to apply **{action_name}** to **{dispute_count}** disputes.")
            st.write("This bulk action will:")
            st.write(f"• Execute {action_name} on all selected cases")
            st.write("• Create individual audit trail entries")
            st.write("• Take 1-2 minutes to complete")
            
            col_confirm, col_cancel = st.columns(2)
            with col_confirm:
                if st.button("✅ Confirm Bulk Action", key="confirm_bulk_action"):
                    st.session_state.show_bulk_action_modal = False
                    return True
            with col_cancel:
                if st.button("❌ Cancel", key="cancel_bulk_action"):
                    st.session_state.show_bulk_action_modal = False
                    return False
            st.markdown("---")
    
    return None


def show_action_success(action_name, details=None):
    """Show success message for completed action."""
    st.success(f"✅ {action_name} completed successfully!")
    if details:
        st.info(details)


def show_action_error(action_name, error_message=None):
    """Show error message for failed action."""
    st.error(f"❌ {action_name} failed!")
    if error_message:
        st.error(f"Error: {error_message}")

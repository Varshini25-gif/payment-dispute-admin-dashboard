"""
Admin service module
Provides admin control operations for disputes, escalations, and assignments.
"""

from app.services.api_client import APIClient


class AdminService(APIClient):
    """Service for admin control operations"""

    # Escalation Operations
    def escalate_dispute(self, dispute_id, escalation_reason, escalation_level):
        """Escalate a dispute to a higher level."""
        data = {
            "dispute_id": dispute_id,
            "reason": escalation_reason,
            "escalation_level": escalation_level
        }
        return self.post("/admin/escalate", data=data)

    def get_escalations(self, status=None, limit=50):
        """Get list of escalated disputes."""
        params = {"limit": limit}
        if status:
            params["status"] = status
        return self.get("/admin/escalations", params=params)

    def resolve_escalation(self, escalation_id, resolution):
        """Resolve an escalation."""
        data = {"resolution": resolution}
        return self.put(f"/admin/escalations/{escalation_id}", data=data)

    # Retry Operations
    def retry_dispute_processing(self, dispute_id, retry_reason):
        """Retry processing of a failed dispute."""
        data = {
            "dispute_id": dispute_id,
            "retry_reason": retry_reason
        }
        return self.post("/admin/retry", data=data)

    def get_retry_history(self, dispute_id):
        """Get retry history for a dispute."""
        return self.get(f"/admin/disputes/{dispute_id}/retry-history")

    def cancel_retry(self, retry_id):
        """Cancel a pending retry operation."""
        return self.delete(f"/admin/retries/{retry_id}")

    # Queue Assignment Operations
    def assign_dispute(self, dispute_id, assignee_id, queue=None):
        """Manually assign a dispute to an agent/queue."""
        data = {
            "dispute_id": dispute_id,
            "assignee_id": assignee_id
        }
        if queue:
            data["queue"] = queue
        return self.put(f"/admin/disputes/{dispute_id}/assign", data=data)

    def get_available_agents(self, queue=None):
        """Get list of available agents for assignment."""
        params = {}
        if queue:
            params["queue"] = queue
        return self.get("/admin/agents/available", params=params)

    def get_queue_status(self, queue=None):
        """Get current queue status and load."""
        params = {}
        if queue:
            params["queue"] = queue
        return self.get("/admin/queues/status", params=params)

    # Override Operations
    def override_dispute_decision(self, dispute_id, override_decision, override_reason):
        """Override the current dispute decision/status."""
        data = {
            "dispute_id": dispute_id,
            "new_decision": override_decision,
            "override_reason": override_reason
        }
        return self.put(f"/admin/disputes/{dispute_id}/override", data=data)

    def get_override_history(self, dispute_id):
        """Get override history for a dispute."""
        return self.get(f"/admin/disputes/{dispute_id}/override-history")

    # Admin Actions Audit
    def get_admin_actions_log(self, admin_id=None, action_type=None, limit=100):
        """Get audit log of admin actions."""
        params = {"limit": limit}
        if admin_id:
            params["admin_id"] = admin_id
        if action_type:
            params["action_type"] = action_type
        return self.get("/admin/actions-log", params=params)

    def log_admin_action(self, action_type, dispute_id, details):
        """Log an admin action for audit trail."""
        data = {
            "action_type": action_type,
            "dispute_id": dispute_id,
            "details": details
        }
        return self.post("/admin/actions-log", data=data)


admin_service = AdminService()

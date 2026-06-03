"""
Dispute service module
Provides dispute-specific API methods for the dashboard.
"""

from app.services.api_client import APIClient


class DisputeService(APIClient):
    """Service for dispute-related API calls"""

    def get_disputes(self, status=None, priority=None, limit=50):
        """Get list of disputes with optional filters."""
        params = {"limit": limit}
        if status and status != "All":
            params["status"] = status
        if priority and priority != "All":
            params["priority"] = priority
        return self.get("/disputes", params=params)

    def get_dispute_by_id(self, dispute_id):
        """Get a single dispute by ID."""
        return self.get(f"/disputes/{dispute_id}")

    def create_dispute(self, dispute_data):
        """Create a new dispute."""
        return self.post("/disputes", data=dispute_data)

    def update_dispute(self, dispute_id, dispute_data):
        """Update an existing dispute."""
        return self.put(f"/disputes/{dispute_id}", data=dispute_data)

    def delete_dispute(self, dispute_id):
        """Delete a dispute by ID."""
        return self.delete(f"/disputes/{dispute_id}")


dispute_service = DisputeService()

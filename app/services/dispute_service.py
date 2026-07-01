"""
Dispute service module
Provides dispute-specific API methods for the dashboard.
"""

from app.services.api_client import APIClient


class DisputeService(APIClient):
    """Service for dispute-related API calls"""

    def get_disputes(
        self,
        status=None,
        priority=None,
        queue=None,
        sla_bucket=None,
        dispute_type=None,
        start_date=None,
        end_date=None,
        search=None,
        limit=50,
    ):
        """Get list of disputes with optional filters."""
        params = {"limit": limit}

        optional_filters = {
            "status": status,
            "priority": priority,
            "queue": queue,
            "sla_bucket": sla_bucket,
            "dispute_type": dispute_type,
            "start_date": start_date,
            "end_date": end_date,
            "search": search,
        }

        for key, value in optional_filters.items():
            if value is None:
                continue
            if isinstance(value, str):
                value = value.strip()
            if value == "" or value == "All":
                continue
            params[key] = value

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

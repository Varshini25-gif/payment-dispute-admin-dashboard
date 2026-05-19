"""
API Client Service
Handles all API communications with the backend
"""

import requests
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
TIMEOUT = int(os.getenv("API_TIMEOUT", 30))


class APIClient:
    """Base API client for making HTTP requests"""
    
    def __init__(self, base_url=BASE_URL, timeout=TIMEOUT):
        self.base_url = base_url
        self.timeout = timeout
    
    def get(self, endpoint, params=None):
        """Make GET request"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"GET request failed: {e}")
            raise
    
    def post(self, endpoint, data=None):
        """Make POST request"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.post(url, json=data, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"POST request failed: {e}")
            raise
    
    def put(self, endpoint, data=None):
        """Make PUT request"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.put(url, json=data, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"PUT request failed: {e}")
            raise
    
    def delete(self, endpoint):
        """Make DELETE request"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.delete(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json() if response.text else None
        except requests.exceptions.RequestException as e:
            logger.error(f"DELETE request failed: {e}")
            raise


class DisputeService(APIClient):
    """Service for dispute-related API calls"""
    
    def get_disputes(self, status=None, priority=None, limit=50):
        """Get list of disputes with optional filters"""
        params = {"limit": limit}
        if status:
            params["status"] = status
        if priority:
            params["priority"] = priority
        return self.get("/disputes", params=params)
    
    def get_dispute_by_id(self, dispute_id):
        """Get specific dispute by ID"""
        return self.get(f"/disputes/{dispute_id}")
    
    def create_dispute(self, dispute_data):
        """Create new dispute"""
        return self.post("/disputes", data=dispute_data)
    
    def update_dispute(self, dispute_id, dispute_data):
        """Update existing dispute"""
        return self.put(f"/disputes/{dispute_id}", data=dispute_data)
    
    def delete_dispute(self, dispute_id):
        """Delete dispute"""
        return self.delete(f"/disputes/{dispute_id}")


class UserService(APIClient):
    """Service for user-related API calls"""
    
    def get_users(self, limit=50):
        """Get list of users"""
        return self.get("/users", params={"limit": limit})
    
    def get_user_by_id(self, user_id):
        """Get specific user by ID"""
        return self.get(f"/users/{user_id}")
    
    def create_user(self, user_data):
        """Create new user"""
        return self.post("/users", data=user_data)
    
    def update_user(self, user_id, user_data):
        """Update existing user"""
        return self.put(f"/users/{user_id}", data=user_data)


# Create singleton instances
api_client = APIClient()
dispute_service = DisputeService()
user_service = UserService()

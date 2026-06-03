"""
API Client Service
Handles all API communications with the backend
"""

import logging
import os

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
TIMEOUT = int(os.getenv("API_TIMEOUT", 30))
DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}


class APIClient:
    """Base API client for making HTTP requests"""

    def __init__(self, base_url=BASE_URL, timeout=TIMEOUT, headers=None):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.headers = {**DEFAULT_HEADERS, **(headers or {})}

    def _request(self, method, endpoint, params=None, json=None):
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(
                method,
                url,
                params=params,
                json=json,
                headers=self.headers,
                timeout=self.timeout,
            )
            response.raise_for_status()
            if response.text:
                return response.json()
            return None
        except requests.exceptions.RequestException as exc:
            logger.error("API request failed: %s %s %s", method, url, exc)
            raise

    def get(self, endpoint, params=None):
        return self._request("get", endpoint, params=params)

    def post(self, endpoint, data=None):
        return self._request("post", endpoint, json=data)

    def put(self, endpoint, data=None):
        return self._request("put", endpoint, json=data)

    def delete(self, endpoint):
        return self._request("delete", endpoint)


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


api_client = APIClient()
user_service = UserService()

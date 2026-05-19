"""
Test Configuration and Fixtures
"""

import pytest
import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def sample_dispute_data():
    """Sample dispute data for testing"""
    return {
        "dispute_id": "DIS-1001",
        "amount": 500.00,
        "status": "pending",
        "priority": "high",
        "customer_id": "CUST-001",
        "created_date": "2024-05-19"
    }


@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "user_id": "USER-001",
        "username": "admin_user",
        "email": "admin@example.com",
        "role": "admin",
        "active": True
    }


@pytest.fixture
def sample_disputes_list():
    """Sample list of disputes"""
    return [
        {
            "dispute_id": f"DIS-{1000+i}",
            "amount": 100.0 * (i+1),
            "status": ["pending", "in_review", "resolved"][i % 3],
            "priority": ["low", "medium", "high"][i % 3],
            "customer_id": f"CUST-{i:03d}",
            "created_date": "2024-05-19"
        }
        for i in range(10)
    ]

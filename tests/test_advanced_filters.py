from datetime import date

import pandas as pd

from app.components.advanced_filters import (
    apply_advanced_dispute_filters,
    build_filter_query_params,
    get_default_dispute_filters,
)


def test_get_default_dispute_filters_merges_persisted_values():
    defaults = get_default_dispute_filters(
        {
            "status": "Pending",
            "queue": "Risk Queue",
            "start_date": "2026-06-01",
            "end_date": "2026-06-15",
        }
    )

    assert defaults["status"] == "Pending"
    assert defaults["queue"] == "Risk Queue"
    assert defaults["start_date"] == date(2026, 6, 1)
    assert defaults["end_date"] == date(2026, 6, 15)


def test_build_filter_query_params_omits_default_values():
    params = build_filter_query_params(
        {
            "search_term": "",
            "status": "All",
            "priority": "High",
            "queue": "All",
            "sla_bucket": "Breach Risk",
            "dispute_type": "All",
            "start_date": date(2026, 6, 1),
            "end_date": date(2026, 6, 30),
        },
        limit=150,
    )

    assert params == {
        "limit": 150,
        "priority": "High",
        "sla_bucket": "Breach Risk",
        "start_date": "2026-06-01",
        "end_date": "2026-06-30",
    }


def test_apply_advanced_dispute_filters_filters_multiple_dimensions():
    data = pd.DataFrame(
        [
            {
                "Dispute ID": "DIS-1001",
                "Customer": "Acme Corp",
                "Status": "Pending",
                "Priority": "High",
                "Queue": "Risk Queue",
                "SLA Bucket": "Breach Risk",
                "Dispute Type": "Fraud",
                "Created": "2026-06-20",
                "Reason": "Unauthorized transaction",
                "Assigned To": "Morgan",
                "Amount": "$500.00",
            },
            {
                "Dispute ID": "DIS-1002",
                "Customer": "Globex",
                "Status": "Resolved",
                "Priority": "Low",
                "Queue": "Operations Queue",
                "SLA Bucket": "Met",
                "Dispute Type": "Refund",
                "Created": "2026-05-10",
                "Reason": "Refund mismatch",
                "Assigned To": "Taylor",
                "Amount": "$250.00",
            },
        ]
    )

    filtered = apply_advanced_dispute_filters(
        data,
        {
            "search_term": "unauthorized",
            "status": "Pending",
            "priority": "High",
            "queue": "Risk Queue",
            "sla_bucket": "Breach Risk",
            "dispute_type": "Fraud",
            "start_date": date(2026, 6, 1),
            "end_date": date(2026, 6, 30),
        },
    )

    assert len(filtered) == 1
    assert filtered.iloc[0]["Dispute ID"] == "DIS-1001"

"""
Audit service module
Provides audit log data with filtering, pagination, and export capabilities.
Uses mock data for demonstration; replace _fetch_all_logs() with real API calls.
"""

import random
import math
from datetime import datetime, timedelta, date
from typing import Optional
import pandas as pd


# ---------------------------------------------------------------------------
# Mock data generation
# ---------------------------------------------------------------------------

_ACTIONS = [
    "Dispute Created", "Dispute Updated", "Status Changed",
    "Document Uploaded", "Agent Assigned", "Comment Added",
    "Dispute Escalated", "Dispute Resolved", "Dispute Closed",
    "Refund Issued", "Evidence Submitted", "Review Requested",
    "User Login", "User Logout", "Export Generated",
]

_ACTORS = [
    "admin@example.com", "agent1@example.com", "agent2@example.com",
    "supervisor@example.com", "system", "john.smith@example.com",
    "sarah.j@example.com",
]

_STATUSES = ["Success", "Warning", "Failure", "Info"]

_STATUS_WEIGHTS = [0.65, 0.15, 0.10, 0.10]

_DISPUTE_IDS = [f"DIS-{n:04d}" for n in range(1000, 1080)]


def _generate_mock_logs(n: int = 500) -> list[dict]:
    rng = random.Random(42)
    base = datetime(2026, 6, 17, 20, 0, 0)
    logs = []
    for i in range(n):
        action = rng.choice(_ACTIONS)
        ts = base - timedelta(
            days=rng.randint(0, 89),
            hours=rng.randint(0, 23),
            minutes=rng.randint(0, 59),
            seconds=rng.randint(0, 59),
        )
        status = rng.choices(_STATUSES, weights=_STATUS_WEIGHTS, k=1)[0]
        dispute_id = rng.choice(_DISPUTE_IDS)
        actor = rng.choice(_ACTORS)
        logs.append({
            "Log ID": f"LOG-{100000 + i:06d}",
            "Timestamp": ts,
            "Dispute ID": dispute_id,
            "Action": action,
            "Actor": actor,
            "Status": status,
            "Details": f"{action} on {dispute_id} by {actor}.",
            "IP Address": f"10.{rng.randint(0,255)}.{rng.randint(0,255)}.{rng.randint(1,254)}",
        })
    logs.sort(key=lambda x: x["Timestamp"], reverse=True)
    return logs


_ALL_LOGS: list[dict] = _generate_mock_logs(500)


# ---------------------------------------------------------------------------
# Public service functions
# ---------------------------------------------------------------------------

def get_audit_logs(
    search_query: str = "",
    dispute_id: str = "All",
    action_filter: str = "All",
    status_filter: str = "All",
    actor_filter: str = "All",
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> pd.DataFrame:
    logs = _ALL_LOGS.copy()

    if search_query:
        q = search_query.lower()
        logs = [
            r for r in logs
            if q in r["Log ID"].lower()
            or q in r["Action"].lower()
            or q in r["Actor"].lower()
            or q in r["Details"].lower()
            or q in r["Dispute ID"].lower()
        ]

    if dispute_id and dispute_id != "All":
        logs = [r for r in logs if r["Dispute ID"] == dispute_id]

    if action_filter != "All":
        logs = [r for r in logs if r["Action"] == action_filter]

    if status_filter != "All":
        logs = [r for r in logs if r["Status"] == status_filter]

    if actor_filter != "All":
        logs = [r for r in logs if r["Actor"] == actor_filter]

    if start_date:
        logs = [r for r in logs if r["Timestamp"].date() >= start_date]

    if end_date:
        logs = [r for r in logs if r["Timestamp"].date() <= end_date]

    df = pd.DataFrame(logs)
    if not df.empty:
        df["Timestamp"] = df["Timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
    return df


def get_paginated_logs(
    df: pd.DataFrame,
    page: int = 1,
    page_size: int = 10,
) -> tuple[pd.DataFrame, dict]:
    total = len(df)
    total_pages = max(1, math.ceil(total / page_size))
    page = max(1, min(page, total_pages))
    start = (page - 1) * page_size
    end = start + page_size
    return df.iloc[start:end].reset_index(drop=True), {
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages,
        "start": start,
        "end": min(end, total),
        "has_prev": page > 1,
        "has_next": page < total_pages,
    }


def get_summary() -> dict:
    df = pd.DataFrame(_ALL_LOGS)
    return {
        "total": len(df),
        "success": int((df["Status"] == "Success").sum()),
        "warning": int((df["Status"] == "Warning").sum()),
        "failure": int((df["Status"] == "Failure").sum()),
        "info": int((df["Status"] == "Info").sum()),
    }


def get_distinct_dispute_ids() -> list[str]:
    return ["All"] + sorted({r["Dispute ID"] for r in _ALL_LOGS})


def get_distinct_actors() -> list[str]:
    return ["All"] + sorted({r["Actor"] for r in _ALL_LOGS})


def get_distinct_actions() -> list[str]:
    return ["All"] + sorted({r["Action"] for r in _ALL_LOGS})


def get_recent_activity(limit: int = 15) -> list[dict]:
    return _ALL_LOGS[:limit]


def export_to_csv(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


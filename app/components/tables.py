import math
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st


def generate_sample_disputes(count=25):
    """Generate deterministic sample disputes for table rendering."""
    statuses = ["Pending", "In Review", "Resolved", "Rejected"]
    priorities = ["High", "Medium", "Low"]
    customers = [
        "Acme Corp",
        "Globex",
        "Initech",
        "Umbrella Corp",
        "Stark Industries",
        "Hooli",
        "Dunder Mifflin",
    ]
    reasons = [
        "Duplicate charge",
        "Unauthorized transaction",
        "Refund mismatch",
        "Cardholder dispute",
        "Processing delay",
        "Chargeback escalation",
        "Fraud review",
    ]
    assigned_to = ["Jordan", "Taylor", "Morgan", "Casey", "Riley"]
    queues = ["Chargeback Queue", "Operations Queue", "Risk Queue", "Escalations Queue", "Refund Queue"]
    sla_buckets = ["On Track", "Breach Risk", "Breached", "Met"]
    dispute_types = ["Chargeback", "Fraud", "Refund", "General"]
    base_date = datetime(2026, 5, 1)

    rows = []
    for index in range(count):
        rows.append({
            "Dispute ID": f"DIS-{1000 + index:04d}",
            "Customer": customers[index % len(customers)],
            "Status": statuses[index % len(statuses)],
            "Priority": priorities[index % len(priorities)],
            "Amount": f"${(index + 1) * 125:,.2f}",
            "Created": (base_date - timedelta(days=index)).strftime("%Y-%m-%d"),
            "Reason": reasons[index % len(reasons)],
            "Assigned To": assigned_to[index % len(assigned_to)],
            "Queue": queues[index % len(queues)],
            "SLA Bucket": sla_buckets[index % len(sla_buckets)],
            "Dispute Type": dispute_types[index % len(dispute_types)],
        })

    return pd.DataFrame(rows)


def filter_disputes(data, search_term="", status=None, priority=None):
    """Filter dispute rows by search text and categorical selectors."""
    filtered = data.copy()

    search_term = (search_term or "").strip().lower()
    if search_term:
        filtered["_search_index"] = filtered.apply(
            lambda row: " ".join(
                str(value).lower()
                for value in [
                    row.get("Dispute ID"),
                    row.get("Customer"),
                    row.get("Reason"),
                    row.get("Amount"),
                    row.get("Assigned To"),
                ]
            ),
            axis=1,
        )
        filtered = filtered[filtered["_search_index"].str.contains(search_term, na=False)].copy()
        filtered = filtered.drop(columns=["_search_index"])

    if status and status != "All":
        filtered = filtered[filtered["Status"] == status]

    if priority and priority != "All":
        filtered = filtered[filtered["Priority"] == priority]

    return filtered.reset_index(drop=True)


def paginate_dataframe(data, page_index=1, page_size=10):
    """Return a paginated dataframe slice and pagination metadata."""
    total_rows = len(data)
    page_index = max(1, int(page_index))
    page_size = max(1, int(page_size))
    total_pages = max(1, math.ceil(total_rows / page_size)) if total_rows else 1
    page_index = min(page_index, total_pages)

    start_index = (page_index - 1) * page_size
    end_index = start_index + page_size
    page = data.iloc[start_index:end_index].reset_index(drop=True)

    return page, {
        "page_index": page_index,
        "page_size": page_size,
        "total_rows": total_rows,
        "total_pages": total_pages,
        "start_index": start_index,
        "end_index": end_index,
        "has_prev": page_index > 1,
        "has_next": page_index < total_pages,
    }


def render_recent_disputes_table(data=None):
    """Render the recent disputes table section."""
    st.subheader("Recent Disputes")
    if data is None:
        data = generate_sample_disputes()
    st.dataframe(data, use_container_width=True, hide_index=True)

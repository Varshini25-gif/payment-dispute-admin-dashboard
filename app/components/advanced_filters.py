"""Advanced dispute filters with persistence-friendly defaults and fast filtering."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Any

import pandas as pd
import streamlit as st


DEFAULT_FILTER_WINDOW_DAYS = 30
DEFAULT_FILTERS = {
    "search_term": "",
    "status": "All",
    "priority": "All",
    "queue": "All",
    "sla_bucket": "All",
    "dispute_type": "All",
}


def _normalize_date(value: Any) -> date | None:
    if value is None or value == "":
        return None
    if isinstance(value, date):
        return value
    parsed = pd.to_datetime(value, errors="coerce")
    if pd.isna(parsed):
        return None
    return parsed.date()


def get_default_dispute_filters(saved_filters: dict[str, Any] | None = None) -> dict[str, Any]:
    """Merge persisted filters with sensible defaults."""
    saved_filters = saved_filters or {}
    today = date.today()
    default_start = today - timedelta(days=DEFAULT_FILTER_WINDOW_DAYS)

    merged = {**DEFAULT_FILTERS, **saved_filters}
    merged["start_date"] = _normalize_date(saved_filters.get("start_date")) or default_start
    merged["end_date"] = _normalize_date(saved_filters.get("end_date")) or today
    return merged


def render_advanced_dispute_filters(
    queue_options: list[str],
    sla_options: list[str],
    dispute_type_options: list[str],
    defaults: dict[str, Any],
    form_key: str = "dispute_advanced_filter_form",
) -> tuple[dict[str, Any], bool]:
    """Render advanced filter form and return active filters plus apply status."""
    status_options = ["All", "Pending", "In Review", "Resolved", "Rejected"]
    priority_options = ["All", "Low", "Medium", "High"]

    def _pick(options: list[str], value: str) -> int:
        return options.index(value) if value in options else 0

    with st.form(form_key, clear_on_submit=False):
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            search_term = st.text_input(
                "Search",
                value=str(defaults.get("search_term", "")),
                placeholder="Dispute ID, customer, reason, assignee",
            )
            status = st.selectbox(
                "Status",
                status_options,
                index=_pick(status_options, str(defaults.get("status", "All"))),
            )

        with col2:
            priority = st.selectbox(
                "Priority",
                priority_options,
                index=_pick(priority_options, str(defaults.get("priority", "All"))),
            )
            queue = st.selectbox(
                "Queue",
                queue_options,
                index=_pick(queue_options, str(defaults.get("queue", "All"))),
            )

        with col3:
            sla_bucket = st.selectbox(
                "SLA",
                sla_options,
                index=_pick(sla_options, str(defaults.get("sla_bucket", "All"))),
            )
            dispute_type = st.selectbox(
                "Dispute Type",
                dispute_type_options,
                index=_pick(dispute_type_options, str(defaults.get("dispute_type", "All"))),
            )

        with col4:
            start_date = st.date_input(
                "Start Date",
                value=defaults.get("start_date"),
            )
            end_date = st.date_input(
                "End Date",
                value=defaults.get("end_date"),
            )

        action_col1, action_col2 = st.columns([1, 1])
        with action_col1:
            applied = st.form_submit_button("Apply Filters", use_container_width=True)
        with action_col2:
            reset = st.form_submit_button("Reset Filters", use_container_width=True)

    if reset:
        return get_default_dispute_filters({}), True

    return {
        "search_term": search_term,
        "status": status,
        "priority": priority,
        "queue": queue,
        "sla_bucket": sla_bucket,
        "dispute_type": dispute_type,
        "start_date": start_date,
        "end_date": end_date,
    }, applied


def build_filter_query_params(filters: dict[str, Any], limit: int = 100) -> dict[str, Any]:
    """Build compact API query params by omitting default/no-op filters."""
    params: dict[str, Any] = {"limit": int(limit)}
    for key in ["status", "priority", "queue", "sla_bucket", "dispute_type"]:
        value = filters.get(key)
        if value and value != "All":
            params[key] = value

    if filters.get("search_term"):
        params["search"] = str(filters["search_term"]).strip()

    if filters.get("start_date"):
        params["start_date"] = filters["start_date"].isoformat()

    if filters.get("end_date"):
        params["end_date"] = filters["end_date"].isoformat()

    return params


def apply_advanced_dispute_filters(data: pd.DataFrame, filters: dict[str, Any]) -> pd.DataFrame:
    """Apply efficient vectorized filtering to dispute data."""
    if data is None or data.empty:
        return pd.DataFrame(columns=list(data.columns) if data is not None else [])

    frame = data.copy()
    mask = pd.Series(True, index=frame.index)

    search_term = str(filters.get("search_term", "")).strip().lower()
    if search_term:
        search_columns = [
            "Dispute ID",
            "Customer",
            "Reason",
            "Amount",
            "Assigned To",
            "Queue",
            "Dispute Type",
        ]
        existing = [col for col in search_columns if col in frame.columns]
        if existing:
            search_space = frame[existing].fillna("").astype(str).agg(" ".join, axis=1).str.lower()
            mask &= search_space.str.contains(search_term, na=False)

    for filter_key, column_name in [
        ("status", "Status"),
        ("priority", "Priority"),
        ("queue", "Queue"),
        ("sla_bucket", "SLA Bucket"),
        ("dispute_type", "Dispute Type"),
    ]:
        value = filters.get(filter_key)
        if value and value != "All" and column_name in frame.columns:
            mask &= frame[column_name].astype(str) == str(value)

    created_series = pd.to_datetime(frame.get("Created"), errors="coerce")

    start_date = filters.get("start_date")
    if start_date is not None:
        start_date = _normalize_date(start_date)
        if start_date is not None:
            mask &= created_series.dt.date >= start_date

    end_date = filters.get("end_date")
    if end_date is not None:
        end_date = _normalize_date(end_date)
        if end_date is not None:
            mask &= created_series.dt.date <= end_date

    filtered = frame.loc[mask].copy()
    if "Created" in filtered.columns:
        filtered["_created_dt"] = pd.to_datetime(filtered["Created"], errors="coerce")
        filtered = filtered.sort_values(by="_created_dt", ascending=False, na_position="last")
        filtered = filtered.drop(columns=["_created_dt"])

    return filtered.reset_index(drop=True)

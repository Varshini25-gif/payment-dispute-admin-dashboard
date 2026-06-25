"""Publication filter controls and dataframe filtering helpers."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

import pandas as pd
import streamlit as st

from app.components.status_badges import normalize_publish_status


def render_publication_filters(
    spaces: list[str] | None = None,
    publishers: list[str] | None = None,
) -> dict[str, Any]:
    """Render Confluence publication filter controls and return current values."""
    spaces = spaces or ["All"]
    publishers = publishers or ["All"]

    today = date.today()
    default_start = today - timedelta(days=30)

    with st.expander("🔍 Filters", expanded=True):
        col1, col2, col3, col4 = st.columns([2, 1.4, 1.2, 1.8])

        with col1:
            search_query = st.text_input(
                "Search",
                placeholder="Publication ID, page title, author, space...",
                key="confluence_search_query",
            )
            status = st.selectbox(
                "Publish status",
                ["All", "Published", "Failed", "In Progress", "Partial", "Unknown"],
                key="confluence_status_filter",
            )

        with col2:
            space_key = st.selectbox(
                "Space",
                spaces,
                key="confluence_space_filter",
            )
            published_by = st.selectbox(
                "Publisher",
                publishers,
                key="confluence_publisher_filter",
            )

        with col3:
            start_date = st.date_input(
                "Start date",
                value=default_start,
                key="confluence_start_date",
            )
            end_date = st.date_input(
                "End date",
                value=today,
                key="confluence_end_date",
            )

        with col4:
            st.markdown("**Quick filters**")
            if st.button("❌ Failed only", use_container_width=True, key="confluence_failed_only"):
                st.session_state["confluence_status_filter"] = "Failed"
                st.rerun()
            if st.button("✅ Published only", use_container_width=True, key="confluence_success_only"):
                st.session_state["confluence_status_filter"] = "Published"
                st.rerun()
            if st.button("🔄 Clear filters", use_container_width=True, key="confluence_clear_filters"):
                st.session_state["confluence_search_query"] = ""
                st.session_state["confluence_status_filter"] = "All"
                st.session_state["confluence_space_filter"] = "All"
                st.session_state["confluence_publisher_filter"] = "All"
                st.session_state["confluence_start_date"] = default_start
                st.session_state["confluence_end_date"] = today
                st.rerun()

    return {
        "search_query": search_query,
        "status": status,
        "space_key": space_key,
        "published_by": published_by,
        "start_date": start_date,
        "end_date": end_date,
    }


def apply_publication_filters(data: pd.DataFrame, filters: dict[str, Any]) -> pd.DataFrame:
    """Apply in-memory filters for publication logs returned by the service layer."""
    if data is None or data.empty:
        return pd.DataFrame(columns=list(data.columns) if data is not None else [])

    frame = data.copy()

    search_query = str(filters.get("search_query", "")).strip().lower()
    if search_query:
        frame["_search"] = frame.apply(
            lambda row: " ".join(
                str(row.get(col, "")).lower()
                for col in ["Publication ID", "Page Title", "Space Key", "Published By", "Publish Status"]
            ),
            axis=1,
        )
        frame = frame[frame["_search"].str.contains(search_query, na=False)].copy()
        frame = frame.drop(columns=["_search"])

    status = filters.get("status", "All")
    if status and status != "All":
        normalized_status = normalize_publish_status(str(status))
        frame = frame[frame["Publish Status"].map(normalize_publish_status) == normalized_status]

    space_key = filters.get("space_key", "All")
    if space_key and space_key != "All":
        frame = frame[frame["Space Key"].astype(str).str.upper() == str(space_key).upper()]

    published_by = filters.get("published_by", "All")
    if published_by and published_by != "All":
        frame = frame[frame["Published By"] == published_by]

    start_date = filters.get("start_date")
    if start_date is not None and "Published At" in frame.columns:
        frame = frame[frame["Published At"].dt.date >= start_date]

    end_date = filters.get("end_date")
    if end_date is not None and "Published At" in frame.columns:
        frame = frame[frame["Published At"].dt.date <= end_date]

    return frame.sort_values(by="Published At", ascending=False).reset_index(drop=True)

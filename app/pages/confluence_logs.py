"""Confluence publication logs page."""

from __future__ import annotations

import streamlit as st

from app.components.publication_filters import apply_publication_filters, render_publication_filters
from app.components.publication_table import render_publication_table
from app.components.status_badges import normalize_publish_status, status_badge_markup
from app.services.confluence_service import confluence_service


def summarize_publication_history(data):
    """Return summary metrics from publication data."""
    if data is None or data.empty:
        return {
            "total": 0,
            "published": 0,
            "failed": 0,
            "in_progress": 0,
            "partial": 0,
        }

    normalized = data["Publish Status"].map(normalize_publish_status)
    counts = normalized.value_counts()
    return {
        "total": int(len(data)),
        "published": int(counts.get("Published", 0)),
        "failed": int(counts.get("Failed", 0)),
        "in_progress": int(counts.get("In Progress", 0)),
        "partial": int(counts.get("Partial", 0)),
    }


def render_status_distribution(summary: dict):
    """Render compact status distribution cards with visual badges."""
    st.subheader("Publish Status Overview")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(status_badge_markup("Published"), unsafe_allow_html=True)
        st.metric("Published", summary.get("published", 0))

    with col2:
        st.markdown(status_badge_markup("Failed"), unsafe_allow_html=True)
        st.metric("Failed", summary.get("failed", 0))

    with col3:
        st.markdown(status_badge_markup("In Progress"), unsafe_allow_html=True)
        st.metric("In Progress", summary.get("in_progress", 0))

    with col4:
        st.markdown(status_badge_markup("Partial"), unsafe_allow_html=True)
        st.metric("Partial", summary.get("partial", 0))


def render() -> None:
    """Render Confluence publication logs page."""
    st.title("📚 Confluence Logs")
    st.markdown(
        "Track Confluence page publication history, statuses, references, "
        "and timestamps with API-backed filtering."
    )
    st.divider()

    spaces = confluence_service.get_distinct_spaces()
    publishers = confluence_service.get_distinct_publishers()

    filters = render_publication_filters(spaces=spaces, publishers=publishers)

    publication_data = confluence_service.get_publication_logs(filters=filters)
    filtered_data = apply_publication_filters(publication_data, filters)

    summary = summarize_publication_history(filtered_data)

    metric_col1, metric_col2, metric_col3 = st.columns([1, 1, 2])
    with metric_col1:
        st.metric("Publication Events", summary["total"])
    with metric_col2:
        success_rate = 0.0
        if summary["total"] > 0:
            success_rate = (summary["published"] / summary["total"]) * 100
        st.metric("Publish Success Rate", f"{success_rate:.1f}%")
    with metric_col3:
        if filtered_data.empty:
            st.caption("No publication events found for the selected filters.")
        else:
            latest = filtered_data.iloc[0]
            st.caption(
                "Latest event: "
                f"{latest.get('Page Title', 'N/A')} "
                f"({latest.get('Published At Display', latest.get('Published At', 'N/A'))})"
            )

    st.divider()
    render_status_distribution(summary)

    st.divider()
    st.subheader("Publication History")
    render_publication_table(filtered_data)

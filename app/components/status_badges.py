"""Status badge helpers for publication states."""

from __future__ import annotations

import streamlit as st


def normalize_publish_status(status: str | None) -> str:
    """Map status aliases to a canonical label used across the UI."""
    value = str(status or "").strip().lower().replace("-", " ").replace("_", " ")
    if value in {"published", "success", "completed"}:
        return "Published"
    if value in {"failed", "error", "errored"}:
        return "Failed"
    if value in {"in progress", "processing", "running"}:
        return "In Progress"
    if value in {"partial", "partially published"}:
        return "Partial"
    return "Unknown"


def status_badge_markup(status: str | None) -> str:
    """Return HTML badge markup for a publish status."""
    normalized = normalize_publish_status(status)
    color_map = {
        "Published": ("#0f5132", "#d1e7dd"),
        "Failed": ("#842029", "#f8d7da"),
        "In Progress": ("#664d03", "#fff3cd"),
        "Partial": ("#084298", "#cfe2ff"),
        "Unknown": ("#41464b", "#e2e3e5"),
    }
    text_color, bg_color = color_map.get(normalized, color_map["Unknown"])
    return (
        f"<span style='background:{bg_color};color:{text_color};"
        "padding:0.18rem 0.52rem;border-radius:999px;font-size:0.75rem;"
        f"font-weight:600;white-space:nowrap;'>{normalized}</span>"
    )


def render_status_badge(status: str | None) -> None:
    """Render a single status badge in Streamlit markdown."""
    st.markdown(status_badge_markup(status), unsafe_allow_html=True)

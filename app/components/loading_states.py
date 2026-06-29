"""Loading and skeleton states for async-like UX feedback."""

from __future__ import annotations

import streamlit as st


def render_skeleton_metrics(count: int = 4) -> None:
    """Render animated skeleton cards used while loading KPI content."""
    cols = st.columns(max(1, count))
    for col in cols:
        with col:
            st.markdown(
                """
                <div class='pd-skeleton-card'>
                    <div class='pd-skeleton-line pd-skeleton-line-icon'></div>
                    <div class='pd-skeleton-line pd-skeleton-line-title'></div>
                    <div class='pd-skeleton-line pd-skeleton-line-value'></div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_chart_loading(message: str = "Loading chart data...") -> None:
    """Render a compact loading line for charts and table sections."""
    st.markdown(
        f"""
        <div class='pd-loading-inline'>
            <span class='pd-loading-dot'></span>
            <span>{message}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def with_spinner(message: str = "Loading..."):
    """Context manager wrapper around Streamlit spinner for consistency."""
    return st.spinner(message)

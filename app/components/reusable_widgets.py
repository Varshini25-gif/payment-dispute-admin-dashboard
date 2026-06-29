"""Reusable widgets for dashboard cards, labels, and empty states."""

from __future__ import annotations

import streamlit as st


def render_kpi_tile(label: str, value: str, delta: str | None = None, icon: str = "") -> None:
    """Render a reusable KPI tile with optional icon and delta text."""
    st.markdown("<div class='pd-kpi-tile'>", unsafe_allow_html=True)
    if icon:
        st.markdown(f"<div class='pd-kpi-icon'>{icon}</div>", unsafe_allow_html=True)
    st.metric(label=label, value=value, delta=delta or "")
    st.markdown("</div>", unsafe_allow_html=True)


def render_chart_container_start(title: str, caption: str | None = None) -> None:
    """Open a chart container shell with consistent title spacing."""
    st.markdown("<div class='pd-chart-card'>", unsafe_allow_html=True)
    st.markdown(f"<h4 class='pd-chart-title'>{title}</h4>", unsafe_allow_html=True)
    if caption:
        st.markdown(f"<p class='pd-chart-caption'>{caption}</p>", unsafe_allow_html=True)


def render_chart_container_end() -> None:
    """Close a chart container shell."""
    st.markdown("</div>", unsafe_allow_html=True)


def render_empty_state(title: str, description: str) -> None:
    """Render a generic empty-state panel."""
    st.markdown(
        f"""
        <div class='pd-empty-state'>
            <h4>{title}</h4>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_action_hint(text: str) -> None:
    """Render muted helper text under controls."""
    st.markdown(f"<p class='pd-action-hint'>{text}</p>", unsafe_allow_html=True)

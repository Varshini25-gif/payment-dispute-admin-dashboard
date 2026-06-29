"""Responsive layout helpers for consistent page structure."""

from __future__ import annotations

import streamlit as st


def render_section_shell(title: str, subtitle: str | None = None) -> None:
    """Render a consistent section heading block."""
    st.markdown("<div class='pd-section-shell'>", unsafe_allow_html=True)
    st.markdown(f"<h3 class='pd-section-title'>{title}</h3>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<p class='pd-section-subtitle'>{subtitle}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def responsive_columns(total_items: int, max_columns: int = 4) -> list:
    """Return a stable number of columns that degrades gracefully on mobile."""
    if total_items <= 0:
        return []
    column_count = max(1, min(total_items, max_columns))
    return st.columns(column_count, gap="medium")


def render_spacer(size: str = "md") -> None:
    """Render vertical rhythm spacing between dashboard blocks."""
    css_class = {
        "sm": "pd-spacer-sm",
        "md": "pd-spacer-md",
        "lg": "pd-spacer-lg",
    }.get(size, "pd-spacer-md")
    st.markdown(f"<div class='{css_class}'></div>", unsafe_allow_html=True)

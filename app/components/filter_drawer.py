"""Reusable filter drawer layout for dispute filters."""

from __future__ import annotations

import streamlit as st


def render_filter_drawer(title: str = "Advanced Filters", expanded: bool = True):
    """Return an expander context manager that behaves like a filter drawer."""
    return st.expander(f"🔎 {title}", expanded=expanded)

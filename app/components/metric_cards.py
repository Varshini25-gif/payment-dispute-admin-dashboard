import streamlit as st

from app.components.loading_states import render_skeleton_metrics
from app.components.responsive_layout import responsive_columns
from app.components.reusable_widgets import render_kpi_tile


def get_dashboard_metrics():
    """Return a list of metric definitions for the dashboard."""
    return [
        {"label": "Total Disputes", "value": "1,234", "delta": "+12 this week", "icon": "📁"},
        {"label": "Pending Disputes", "value": "456", "delta": "-8 this week", "icon": "⏳"},
        {"label": "Resolved Disputes", "value": "678", "delta": "+20 this week", "icon": "✅"},
        {"label": "Resolution Rate", "value": "86.5%", "delta": "+2.3%", "icon": "📈"}
    ]


def render_metric_cards(metrics):
    """Render reusable metric cards in a responsive row."""
    if not metrics:
        render_skeleton_metrics(count=4)
        return

    cols = responsive_columns(total_items=len(metrics), max_columns=4)
    for metric, col in zip(metrics, cols):
        with col:
            render_kpi_tile(
                label=metric["label"],
                value=metric["value"],
                delta=metric.get("delta", ""),
                icon=metric.get("icon", ""),
            )

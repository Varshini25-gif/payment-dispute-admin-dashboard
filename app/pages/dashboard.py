import streamlit as st
import pandas as pd

from app.components.charts import render_status_chart, render_priority_chart, render_volume_chart
from app.components.loading_states import render_chart_loading
from app.components.metric_cards import get_dashboard_metrics, render_metric_cards
from app.components.responsive_layout import render_section_shell, render_spacer, responsive_columns
from app.components.reusable_widgets import render_kpi_tile
from app.components.tables import render_recent_disputes_table


def render_queue_overview_cards():
    """Render queue health cards for the dashboard."""
    render_section_shell("Queue Overview", "Live operational counters for triage and handling capacity.")

    queue_metrics = [
        {"label": "Open Queue", "value": "142", "delta": "12 new today", "icon": "📥"},
        {"label": "Escalations", "value": "18", "delta": "3 high priority", "icon": "🚨"},
        {"label": "Avg. Handling Time", "value": "2.4h", "delta": "-0.3h", "icon": "⏱️"},
        {"label": "Agent Capacity", "value": "87%", "delta": "5 agents online", "icon": "👥"},
    ]

    cols = responsive_columns(total_items=len(queue_metrics), max_columns=4)
    for metric, col in zip(queue_metrics, cols):
        with col:
            render_kpi_tile(
                label=metric["label"],
                value=metric["value"],
                delta=metric["delta"],
                icon=metric["icon"],
            )


def render_sla_placeholder_chart():
    """Render a placeholder SLA chart for the dashboard."""
    render_section_shell("SLA Placeholder", "Sample responsiveness trend for queue monitoring.")

    sla_data = pd.DataFrame(
        {
            "Hour": ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00"],
            "On Time": [89, 91, 87, 93, 95, 92],
            "At Risk": [11, 9, 13, 7, 5, 8],
        }
    )

    st.line_chart(sla_data.set_index("Hour"), use_container_width=True)
    st.caption("Placeholder SLA trend for response and resolution targets.")


def render_alerts_section():
    """Render dashboard alerts section."""
    render_section_shell("Alerts", "Latest actionable notices across queues and SLA health.")

    alerts = [
        "High-priority dispute batch requires manual review before 3:00 PM.",
        "3 cases are approaching SLA breach in the escalation queue.",
        "Payment verification backlog increased by 8% over the last 24 hours.",
    ]

    for alert in alerts:
        st.warning(f"⚠️ {alert}")


def render():
    """Render the dashboard page."""
    st.header("📊 Dashboard")
    st.markdown("High-level dispute insights, queue health, and operational performance.")

    render_section_shell("Dashboard Metrics", "Top-level metrics with week-over-week movement.")
    render_metric_cards(get_dashboard_metrics())
    render_spacer("md")

    render_queue_overview_cards()
    render_spacer("md")

    render_section_shell("Operational Overview", "Recent disputes and category distributions.")
    col1, col2 = st.columns([2, 1])

    with col1:
        render_recent_disputes_table()

    with col2:
        render_chart_loading("Rendering charts...")
        render_status_chart()
        render_priority_chart()
        render_volume_chart()

    render_spacer("md")
    render_sla_placeholder_chart()

    render_spacer("md")
    render_alerts_section()

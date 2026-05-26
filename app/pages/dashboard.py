import streamlit as st
import pandas as pd

from app.components.charts import render_status_chart, render_priority_chart, render_volume_chart
from app.components.metric_cards import get_dashboard_metrics, render_metric_cards
from app.components.tables import render_recent_disputes_table


def render_queue_overview_cards():
    """Render queue health cards for the dashboard."""
    st.subheader("Queue Overview")

    queue_metrics = [
        {"label": "Open Queue", "value": "142", "delta": "12 new today", "icon": "📥"},
        {"label": "Escalations", "value": "18", "delta": "3 high priority", "icon": "🚨"},
        {"label": "Avg. Handling Time", "value": "2.4h", "delta": "-0.3h", "icon": "⏱️"},
        {"label": "Agent Capacity", "value": "87%", "delta": "5 agents online", "icon": "👥"},
    ]

    cols = st.columns(len(queue_metrics))
    for metric, col in zip(queue_metrics, cols):
        with col:
            st.markdown(
                "<div style='background: #f8fafc; padding: 16px; border-radius: 12px; min-height: 140px;'>",
                unsafe_allow_html=True,
            )
            st.markdown(f"<div style='font-size: 24px; margin-bottom: 8px;'>{metric['icon']}</div>", unsafe_allow_html=True)
            st.metric(label=metric["label"], value=metric["value"], delta=metric["delta"])
            st.markdown("</div>", unsafe_allow_html=True)


def render_sla_placeholder_chart():
    """Render a placeholder SLA chart for the dashboard."""
    st.subheader("SLA Placeholder")

    sla_data = pd.DataFrame(
        {
            "Hour": ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00"],
            "On Time": [89, 91, 87, 93, 95, 92],
            "At Risk": [11, 9, 13, 7, 5, 8],
        }
    )

    st.line_chart(sla_data.set_index("Hour"))
    st.caption("Placeholder SLA trend for response and resolution targets.")


def render_alerts_section():
    """Render dashboard alerts section."""
    st.subheader("Alerts")

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

    st.subheader("Dashboard Metrics")
    render_metric_cards(get_dashboard_metrics())

    st.markdown("---")
    render_queue_overview_cards()

    st.markdown("---")
    st.subheader("Operational Overview")
    col1, col2 = st.columns([2, 1])

    with col1:
        render_recent_disputes_table()

    with col2:
        render_status_chart()
        render_priority_chart()
        render_volume_chart()

    st.markdown("---")
    render_sla_placeholder_chart()

    st.markdown("---")
    render_alerts_section()

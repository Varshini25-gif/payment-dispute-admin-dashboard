import streamlit as st
from app.components.charts import render_status_chart, render_priority_chart, render_volume_chart
from app.components.metric_cards import get_dashboard_metrics, render_metric_cards
from app.components.tables import render_recent_disputes_table
from app.components.common import render_info_box


def render():
    """Render the dashboard page."""
    st.header("📊 Dashboard")
    st.markdown("High-level dispute insights, queue health, and operational performance.")

    render_metric_cards(get_dashboard_metrics())

    st.markdown("---")
    st.subheader("Overview")
    st.write("Quickly review active case counts, resolution velocity, and priority trends.")

    col1, col2 = st.columns([2, 1])
    with col1:
        render_recent_disputes_table()
    with col2:
        render_status_chart()
        render_priority_chart()
        render_volume_chart()

    st.markdown("---")
    render_info_box(
        "Dashboard Placeholders",
        "Widgets for workflow actions, live alerts, and drill-down analytics will be added here as the application expands."
    )

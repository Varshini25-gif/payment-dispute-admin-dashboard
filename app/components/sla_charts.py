"""SLA chart components."""

import pandas as pd
import streamlit as st


def render_breach_trend_chart(breach_trends):
    """Render line chart for SLA breach trends."""
    st.subheader("Breach Trend")
    if not breach_trends:
        st.info("No breach trend data available.")
        return

    breach_df = pd.DataFrame(breach_trends)
    st.line_chart(breach_df.set_index("label")["breaches"], use_container_width=True)
    st.caption("Daily trend of SLA breaches across monitored queues.")


def render_resolution_time_chart(resolution_times):
    """Render chart for average and P95 resolution times."""
    st.subheader("Resolution Time Trend")
    if not resolution_times:
        st.info("No resolution time data available.")
        return

    resolution_df = pd.DataFrame(resolution_times)
    chart_df = resolution_df.set_index("label")[["avg_hours", "p95_hours"]]
    chart_df.columns = ["Average Hours", "P95 Hours"]
    st.area_chart(chart_df, use_container_width=True)
    st.caption("Average and P95 resolution time trend by day.")

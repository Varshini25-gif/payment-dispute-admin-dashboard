"""Queue health metric components for SLA monitoring."""

import pandas as pd
import streamlit as st


def render_queue_health_metrics(queue_health):
    """Render queue health metrics and detail table."""
    st.subheader("Queue Health Metrics")
    if not queue_health:
        st.info("No queue health data available.")
        return

    queue_df = pd.DataFrame(queue_health)

    total_open = int(queue_df["open_cases"].sum())
    total_at_risk = int(queue_df["at_risk_cases"].sum())
    avg_on_time = float(queue_df["on_time_pct"].mean())
    critical_queues = int((queue_df["status"].str.lower() == "critical").sum())

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Open Cases", total_open)
    with col2:
        st.metric("At-risk Cases", total_at_risk)
    with col3:
        st.metric("Avg On-time", f"{avg_on_time:.1f}%")
    with col4:
        st.metric("Critical Queues", critical_queues)

    st.dataframe(
        queue_df.rename(
            columns={
                "queue": "Queue",
                "slo_target_pct": "Target %",
                "on_time_pct": "On-time %",
                "open_cases": "Open Cases",
                "at_risk_cases": "At-risk Cases",
                "status": "Status",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

import pandas as pd
import streamlit as st

from app.components.common import render_info_box


def build_routing_queue_distribution():
    """Return a deterministic queue distribution dataset for routing analytics."""
    data = pd.DataFrame(
        {
            "Queue": ["Fraud Review", "Cardholder Support", "Auto Approval", "Escalation Desk"],
            "Volume": [42, 31, 24, 17],
        }
    )
    data["Share"] = (data["Volume"] / data["Volume"].sum() * 100).round(1)
    return data


def build_routing_metrics():
    """Return routing KPI values used by the analytics page."""
    return {
        "auto_approved": 184,
        "manual_review": 73,
        "escalated": 19,
        "avg_decision_time": 3.2,
        "success_rate": 94.8,
    }


def build_decision_summary():
    """Return a summary of decisions by priority tier."""
    data = pd.DataFrame(
        {
            "Priority": ["High", "Medium", "Low"],
            "Decisions": [58, 126, 92],
        }
    )
    data["Share"] = (data["Decisions"] / data["Decisions"].sum() * 100).round(1)
    return data


def build_routing_history():
    """Return recent routing history rows for the analytics dashboard."""
    return pd.DataFrame(
        [
            {"Timestamp": "2026-06-09 08:14", "Case ID": "DIS-1042", "Queue": "Fraud Review", "Decision": "Manual review", "Outcome": "Escalated"},
            {"Timestamp": "2026-06-09 08:27", "Case ID": "DIS-1043", "Queue": "Auto Approval", "Decision": "Auto-route", "Outcome": "Approved"},
            {"Timestamp": "2026-06-09 08:41", "Case ID": "DIS-1044", "Queue": "Cardholder Support", "Decision": "Human review", "Outcome": "Pending"},
            {"Timestamp": "2026-06-09 08:53", "Case ID": "DIS-1045", "Queue": "Escalation Desk", "Decision": "Priority override", "Outcome": "Resolved"},
            {"Timestamp": "2026-06-09 09:02", "Case ID": "DIS-1046", "Queue": "Fraud Review", "Decision": "Policy match", "Outcome": "Escalated"},
        ]
    )


def render():
    """Render the routing analytics dashboard."""
    st.header("🧭 Routing Analytics")
    st.markdown("Monitor queue distribution, routing KPIs, decision outcomes, and recent workflow history.")

    render_info_box(
        "Routing insight",
        "This page combines queue load, routing efficiency, and decision summaries into one operational view."
    )

    metrics = build_routing_metrics()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Auto-approved", metrics["auto_approved"])
    with col2:
        st.metric("Manual review", metrics["manual_review"])
    with col3:
        st.metric("Escalated", metrics["escalated"])
    with col4:
        st.metric("Avg. decision time", f"{metrics['avg_decision_time']} min")

    st.markdown("---")
    st.subheader("Queue distribution charts")
    queue_data = build_routing_queue_distribution()
    chart_col, summary_col = st.columns([1.6, 1])

    with chart_col:
        st.bar_chart(queue_data.set_index("Queue"))

    with summary_col:
        st.dataframe(queue_data, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("Routing metrics")
    metric_col1, metric_col2 = st.columns(2)
    with metric_col1:
        st.metric("Success rate", f"{metrics['success_rate']}%", delta="+1.4% vs prior week")
    with metric_col2:
        st.metric("Routing volume", metrics["auto_approved"] + metrics["manual_review"] + metrics["escalated"])

    st.markdown("---")
    st.subheader("Decision summaries")
    decision_summary = build_decision_summary()
    st.dataframe(decision_summary, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("Routing history tables")
    st.dataframe(build_routing_history(), use_container_width=True, hide_index=True)

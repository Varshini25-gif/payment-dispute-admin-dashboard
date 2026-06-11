import pandas as pd
import streamlit as st

from app.components.metric_cards import render_metric_cards


def build_sla_trend_data():
    """Return deterministic SLA trend data for the monitor page."""
    return pd.DataFrame(
        {
            "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "Response SLA %": [91, 89, 93, 88, 95, 90, 92],
            "Resolution SLA %": [87, 90, 86, 91, 94, 89, 92],
            "Breaches": [3, 4, 2, 5, 1, 3, 2],
        }
    )


def build_queue_sla_table():
    """Return deterministic queue SLA performance rows."""
    return pd.DataFrame(
        [
            {"Queue": "Fraud Review", "SLA %": 88, "Breaches": 5, "Status": "At risk"},
            {"Queue": "Cardholder Support", "SLA %": 92, "Breaches": 2, "Status": "Stable"},
            {"Queue": "Auto Approval", "SLA %": 97, "Breaches": 0, "Status": "Healthy"},
            {"Queue": "Escalation Desk", "SLA %": 81, "Breaches": 7, "Status": "Critical"},
        ]
    )


def build_alerts():
    """Return actionable SLA alerts for the monitor page."""
    return [
        "⚠️ Escalation Desk has 7 breaches and needs immediate agent reassignment.",
        "⚠️ Fraud Review is now 12% below the weekly response SLA target.",
        "⚠️ Two high-value disputes are approaching the 4-hour resolution threshold.",
        "⚠️ Cardholder Support is trending upward; monitor noon shift capacity.",
    ]


def render():
    """Render the SLA monitor dashboard page."""
    st.header("⌚ SLA Monitor")
    st.markdown("Track SLA compliance, queue health, and active breaches in one place.")

    sla_metrics = [
        {"label": "On-time Response", "value": "91%", "delta": "+3% vs last week", "icon": "⏱️"},
        {"label": "Resolution SLA", "value": "89%", "delta": "-1% from target", "icon": "✅"},
        {"label": "Open Breaches", "value": "17", "delta": "5 critical", "icon": "🚨"},
        {"label": "Escalated Cases", "value": "8", "delta": "2 pending review", "icon": "📈"},
    ]

    st.subheader("SLA overview")
    render_metric_cards(sla_metrics)

    st.markdown("---")
    st.subheader("SLA charts")

    trend_data = build_sla_trend_data()
    queue_sla = build_queue_sla_table()

    col1, col2 = st.columns([2, 1])
    with col1:
        st.line_chart(trend_data.set_index("Day")["Response SLA %"], use_container_width=True)
        st.caption("Weekly response SLA trend across each day of the reporting window.")

    with col2:
        st.bar_chart(trend_data.set_index("Day")["Breaches"], use_container_width=True)
        st.caption("Count of SLA breaches by day for quick escalation spotting.")

    st.markdown("---")
    st.subheader("Breach indicators")
    indicator_cols = st.columns(3)
    for indicator, column in zip(
        [
            ("Critical queues", "Escalation Desk", "2 queues above threshold"),
            ("At-risk cases", "17 open", "5 will breach within 2 hours"),
            ("Compliance score", "89%", "Target is 92%"),
        ],
        indicator_cols,
    ):
        with column:
            st.markdown(
                "<div style='background: #fff7ed; padding: 16px; border-radius: 12px; border: 1px solid #fed7aa;'>"
                f"<strong>{indicator[0]}</strong><br/>{indicator[1]}<br/><span style='color:#b45309;'>{indicator[2]}</span>"
                "</div>",
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.subheader("Queue SLA table")
    st.dataframe(queue_sla, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("Alerts")
    for alert in build_alerts():
        st.warning(alert)

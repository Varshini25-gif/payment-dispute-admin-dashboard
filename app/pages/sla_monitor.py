import streamlit as st

from app.components.breach_cards import render_sla_summary_cards
from app.components.queue_metrics import render_queue_health_metrics
from app.components.sla_charts import render_breach_trend_chart, render_resolution_time_chart
from app.services.sla_service import sla_service

try:
    from streamlit_autorefresh import st_autorefresh
except ImportError:  # pragma: no cover - optional dependency in local dev
    st_autorefresh = None

def _apply_real_time_refresh():
    """Configure optional real-time refresh for SLA data."""
    refresh_enabled = st.toggle("Enable real-time refresh", value=True)
    refresh_seconds = st.selectbox("Refresh interval", [15, 30, 60, 120], index=1)

    if refresh_enabled and st_autorefresh is not None:
        st_autorefresh(interval=refresh_seconds * 1000, key="sla-auto-refresh")
    elif refresh_enabled:
        st.info("Install `streamlit-autorefresh` to enable automatic refresh ticks.")


def _build_alerts(queue_health, summary):
    """Generate actionable SLA alerts from live queue and summary data."""
    alerts = []
    critical_queues = [queue for queue in queue_health if str(queue.get("status", "")).lower() == "critical"]
    if critical_queues:
        queue_names = ", ".join(queue["queue"] for queue in critical_queues)
        alerts.append(f"Critical queue detected: {queue_names}. Prioritize workload balancing.")

    open_breaches = int(summary.get("open_breaches", 0))
    if open_breaches > 0:
        alerts.append(f"There are currently {open_breaches} open SLA breaches requiring triage.")

    avg_resolution_hours = float(summary.get("avg_resolution_hours", 0.0))
    if avg_resolution_hours > 4.5:
        alerts.append("Average resolution time is elevated; review bottlenecks in escalation paths.")

    if not alerts:
        alerts.append("All SLA indicators are stable. Continue monitoring for queue spikes.")
    return alerts


def render():
    """Render the SLA monitor dashboard page."""
    st.header("⌚ SLA Monitor")
    st.markdown("Track SLA compliance with live breach trends, resolution performance, and queue health metrics.")

    controls_col, refresh_col = st.columns([3, 1])
    with controls_col:
        days = st.selectbox("Window", [7, 14, 30], index=0)
    with refresh_col:
        st.button("Refresh now")

    _apply_real_time_refresh()

    dashboard_data = sla_service.get_dashboard_data(days=days)
    if dashboard_data.get("is_fallback"):
        st.warning("Showing sample SLA data because the SLA API is unavailable.")

    summary = dashboard_data["summary"]
    breach_trends = dashboard_data["breach_trends"]
    resolution_times = dashboard_data["resolution_times"]
    queue_health = dashboard_data["queue_health"]

    st.subheader("SLA Summary")
    render_sla_summary_cards(summary)

    st.markdown("---")
    st.subheader("SLA Trends")

    col1, col2 = st.columns([2, 1])
    with col1:
        render_breach_trend_chart(breach_trends)

    with col2:
        render_resolution_time_chart(resolution_times)

    st.markdown("---")
    render_queue_health_metrics(queue_health)

    st.markdown("---")
    st.subheader("Alerts")
    for alert in _build_alerts(queue_health, summary):
        st.warning(f"⚠️ {alert}")

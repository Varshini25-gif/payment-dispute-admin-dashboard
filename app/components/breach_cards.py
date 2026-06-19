"""SLA summary card components."""

from app.components.metric_cards import render_metric_cards


def render_sla_summary_cards(summary):
    """Render summary cards for SLA key indicators."""
    on_time_rate = summary.get("on_time_rate", 0.0)
    resolution_sla_rate = summary.get("resolution_sla_rate", 0.0)
    open_breaches = summary.get("open_breaches", 0)
    avg_resolution_hours = summary.get("avg_resolution_hours", 0.0)

    cards = [
        {
            "label": "On-time Response",
            "value": f"{on_time_rate:.1f}%",
            "delta": "Target 92%",
            "icon": "⏱️",
        },
        {
            "label": "Resolution SLA",
            "value": f"{resolution_sla_rate:.1f}%",
            "delta": "Target 90%",
            "icon": "✅",
        },
        {
            "label": "Open Breaches",
            "value": str(open_breaches),
            "delta": "Needs triage",
            "icon": "🚨",
        },
        {
            "label": "Avg Resolution",
            "value": f"{avg_resolution_hours:.1f}h",
            "delta": "Rolling 7 days",
            "icon": "📉",
        },
    ]
    render_metric_cards(cards)

import app.pages.sla_monitor as sla_monitor
from app.pages.sla_monitor import _build_alerts


def test_build_alerts_returns_generated_messages():
    queue_health = [
        {"queue": "Escalation Desk", "status": "Critical"},
        {"queue": "Fraud Review", "status": "At risk"},
    ]
    summary = {"open_breaches": 5, "avg_resolution_hours": 4.8}

    alerts = _build_alerts(queue_health, summary)

    assert isinstance(alerts, list)
    assert len(alerts) >= 2
    assert any("Critical queue" in alert for alert in alerts)
    assert any("open SLA breaches" in alert for alert in alerts)


def test_render_runs_without_error(monkeypatch):
    class DummyColumn:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    class DummyStreamlit:
        def header(self, *args, **kwargs):
            return None

        def markdown(self, *args, **kwargs):
            return None

        def subheader(self, *args, **kwargs):
            return None

        def columns(self, *args, **kwargs):
            if args and isinstance(args[0], (list, tuple)):
                return [DummyColumn() for _ in args[0]]
            count = args[0] if args else 1
            return [DummyColumn() for _ in range(count)]

        def metric(self, *args, **kwargs):
            return None

        def line_chart(self, *args, **kwargs):
            return None

        def bar_chart(self, *args, **kwargs):
            return None

        def area_chart(self, *args, **kwargs):
            return None

        def dataframe(self, *args, **kwargs):
            return None

        def warning(self, *args, **kwargs):
            return None

        def caption(self, *args, **kwargs):
            return None

        def button(self, *args, **kwargs):
            return False

        def toggle(self, *args, **kwargs):
            return False

        def selectbox(self, *args, **kwargs):
            options = args[1] if len(args) > 1 else kwargs.get("options", [])
            return options[0] if options else None

        def info(self, *args, **kwargs):
            return None

    monkeypatch.setattr(sla_monitor, "st", DummyStreamlit())
    monkeypatch.setattr(sla_monitor, "st_autorefresh", None)
    monkeypatch.setattr(sla_monitor, "render_sla_summary_cards", lambda summary: None)
    monkeypatch.setattr(sla_monitor, "render_breach_trend_chart", lambda trends: None)
    monkeypatch.setattr(sla_monitor, "render_resolution_time_chart", lambda times: None)
    monkeypatch.setattr(sla_monitor, "render_queue_health_metrics", lambda queue_health: None)
    monkeypatch.setattr(
        sla_monitor.sla_service,
        "get_dashboard_data",
        lambda days=7: {
            "summary": {
                "on_time_rate": 91.2,
                "resolution_sla_rate": 88.6,
                "open_breaches": 4,
                "avg_resolution_hours": 4.1,
            },
            "breach_trends": [{"label": "Mon", "breaches": 3}],
            "resolution_times": [{"label": "Mon", "avg_hours": 4.1, "p95_hours": 6.0}],
            "queue_health": [
                {
                    "queue": "Escalation Desk",
                    "slo_target_pct": 94,
                    "on_time_pct": 89,
                    "open_cases": 12,
                    "at_risk_cases": 3,
                    "status": "At risk",
                }
            ],
            "is_fallback": False,
        },
    )

    sla_monitor.render()

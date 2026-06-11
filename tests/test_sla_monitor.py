import pandas as pd

import app.pages.sla_monitor as sla_monitor
from app.pages.sla_monitor import (
    build_alerts,
    build_queue_sla_table,
    build_sla_trend_data,
)


def test_build_sla_trend_data_returns_expected_columns():
    data = build_sla_trend_data()

    assert isinstance(data, pd.DataFrame)
    assert list(data.columns) == ["Day", "Response SLA %", "Resolution SLA %", "Breaches"]
    assert len(data) == 7


def test_build_queue_sla_table_returns_priority_and_breaches():
    data = build_queue_sla_table()

    assert isinstance(data, pd.DataFrame)
    assert {"Queue", "SLA %", "Breaches", "Status"}.issubset(set(data.columns))
    assert len(data) >= 4


def test_build_alerts_returns_actionable_items():
    alerts = build_alerts()

    assert isinstance(alerts, list)
    assert len(alerts) >= 3
    assert all("⚠️" in alert for alert in alerts)


def test_render_accepts_page_name_and_runs_without_error(monkeypatch):
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

        def dataframe(self, *args, **kwargs):
            return None

        def warning(self, *args, **kwargs):
            return None

        def caption(self, *args, **kwargs):
            return None

    monkeypatch.setattr(sla_monitor, "st", DummyStreamlit())
    monkeypatch.setattr(sla_monitor, "render_metric_cards", lambda metrics: None)

    sla_monitor.render()

import pandas as pd

from app.pages.routing_analytics import (
    build_decision_summary,
    build_routing_history,
    build_routing_metrics,
    build_routing_queue_distribution,
)


def test_build_routing_queue_distribution_returns_expected_columns():
    data = build_routing_queue_distribution()

    assert isinstance(data, pd.DataFrame)
    assert list(data.columns) == ["Queue", "Volume", "Share"]
    assert data["Volume"].sum() > 0


def test_build_routing_metrics_returns_key_indicators():
    metrics = build_routing_metrics()

    assert set(metrics) >= {"auto_approved", "manual_review", "escalated", "avg_decision_time", "success_rate"}
    assert metrics["auto_approved"] >= 0
    assert 0 <= metrics["success_rate"] <= 100


def test_build_decision_summary_returns_priority_breakdown():
    summary = build_decision_summary()

    assert isinstance(summary, pd.DataFrame)
    assert list(summary.columns) == ["Priority", "Decisions", "Share"]
    assert summary["Decisions"].sum() > 0


def test_build_routing_history_returns_recent_events():
    history = build_routing_history()

    assert isinstance(history, pd.DataFrame)
    assert list(history.columns) == ["Timestamp", "Case ID", "Queue", "Decision", "Outcome"]
    assert len(history) >= 5

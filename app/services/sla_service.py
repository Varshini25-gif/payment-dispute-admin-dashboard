"""
SLA service module
Provides SLA monitoring API methods and normalized dashboard datasets.
"""

from __future__ import annotations

import logging
from typing import Any

from app.services.api_client import APIClient

logger = logging.getLogger(__name__)


class SLAService(APIClient):
    """Service for SLA-related API calls."""

    def get_sla_summary(self) -> dict[str, Any]:
        """Get aggregate SLA summary cards."""
        return self.get("/sla/summary")

    def get_breach_trends(self, days: int = 7) -> dict[str, Any]:
        """Get breach trend data over the requested period."""
        return self.get("/sla/breach-trends", params={"days": days})

    def get_resolution_times(self, days: int = 7) -> dict[str, Any]:
        """Get resolution time trend data over the requested period."""
        return self.get("/sla/resolution-times", params={"days": days})

    def get_queue_health(self) -> dict[str, Any]:
        """Get queue-level SLA health metrics."""
        return self.get("/sla/queue-health")

    def get_dashboard_data(self, days: int = 7) -> dict[str, Any]:
        """
        Get all SLA dashboard data in one normalized payload.

        Falls back to deterministic sample data if API calls fail.
        """
        try:
            summary = self.get_sla_summary()
            breach_trends = self.get_breach_trends(days=days)
            resolution_times = self.get_resolution_times(days=days)
            queue_health = self.get_queue_health()
            return {
                "summary": self._normalize_summary(summary),
                "breach_trends": self._normalize_breach_trends(breach_trends),
                "resolution_times": self._normalize_resolution_times(resolution_times),
                "queue_health": self._normalize_queue_health(queue_health),
                "is_fallback": False,
            }
        except Exception as exc:
            logger.warning("Falling back to local SLA sample data: %s", exc)
            return self.get_sample_dashboard_data(days=days)

    def get_sample_dashboard_data(self, days: int = 7) -> dict[str, Any]:
        """Return deterministic sample data for local/dev mode."""
        labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        labels = labels[:max(1, min(days, len(labels)))]

        return {
            "summary": {
                "on_time_rate": 91.6,
                "resolution_sla_rate": 88.9,
                "open_breaches": 17,
                "avg_resolution_hours": 4.2,
            },
            "breach_trends": [
                {"label": labels[0], "breaches": 4},
                {"label": labels[1], "breaches": 6},
                {"label": labels[2], "breaches": 3},
                {"label": labels[3], "breaches": 5},
                {"label": labels[4], "breaches": 2},
                {"label": labels[5], "breaches": 4},
                {"label": labels[6], "breaches": 3},
            ][: len(labels)],
            "resolution_times": [
                {"label": labels[0], "avg_hours": 4.9, "p95_hours": 7.2},
                {"label": labels[1], "avg_hours": 4.6, "p95_hours": 6.9},
                {"label": labels[2], "avg_hours": 4.4, "p95_hours": 6.4},
                {"label": labels[3], "avg_hours": 4.7, "p95_hours": 6.8},
                {"label": labels[4], "avg_hours": 4.0, "p95_hours": 6.1},
                {"label": labels[5], "avg_hours": 4.2, "p95_hours": 6.3},
                {"label": labels[6], "avg_hours": 3.8, "p95_hours": 5.9},
            ][: len(labels)],
            "queue_health": [
                {
                    "queue": "Fraud Review",
                    "slo_target_pct": 92,
                    "on_time_pct": 88,
                    "open_cases": 46,
                    "at_risk_cases": 8,
                    "status": "At risk",
                },
                {
                    "queue": "Cardholder Support",
                    "slo_target_pct": 90,
                    "on_time_pct": 93,
                    "open_cases": 34,
                    "at_risk_cases": 2,
                    "status": "Healthy",
                },
                {
                    "queue": "Auto Approval",
                    "slo_target_pct": 95,
                    "on_time_pct": 97,
                    "open_cases": 28,
                    "at_risk_cases": 1,
                    "status": "Healthy",
                },
                {
                    "queue": "Escalation Desk",
                    "slo_target_pct": 94,
                    "on_time_pct": 83,
                    "open_cases": 22,
                    "at_risk_cases": 9,
                    "status": "Critical",
                },
            ],
            "is_fallback": True,
        }

    def _normalize_summary(self, payload: Any) -> dict[str, Any]:
        data = payload or {}
        return {
            "on_time_rate": float(data.get("on_time_rate", data.get("response_sla_pct", 0.0))),
            "resolution_sla_rate": float(data.get("resolution_sla_rate", data.get("resolution_sla_pct", 0.0))),
            "open_breaches": int(data.get("open_breaches", data.get("breaches", 0))),
            "avg_resolution_hours": float(data.get("avg_resolution_hours", data.get("avg_resolution_time_hours", 0.0))),
        }

    def _normalize_breach_trends(self, payload: Any) -> list[dict[str, Any]]:
        if isinstance(payload, dict):
            payload = payload.get("items", [])
        items = payload or []
        normalized = []
        for item in items:
            normalized.append(
                {
                    "label": str(item.get("label", item.get("day", item.get("date", "N/A")))),
                    "breaches": int(item.get("breaches", item.get("count", 0))),
                }
            )
        return normalized

    def _normalize_resolution_times(self, payload: Any) -> list[dict[str, Any]]:
        if isinstance(payload, dict):
            payload = payload.get("items", [])
        items = payload or []
        normalized = []
        for item in items:
            normalized.append(
                {
                    "label": str(item.get("label", item.get("day", item.get("date", "N/A")))),
                    "avg_hours": float(item.get("avg_hours", item.get("avg_resolution_hours", 0.0))),
                    "p95_hours": float(item.get("p95_hours", item.get("p95_resolution_hours", 0.0))),
                }
            )
        return normalized

    def _normalize_queue_health(self, payload: Any) -> list[dict[str, Any]]:
        if isinstance(payload, dict):
            payload = payload.get("items", [])
        items = payload or []
        normalized = []
        for item in items:
            normalized.append(
                {
                    "queue": str(item.get("queue", item.get("queue_name", "Unknown"))),
                    "slo_target_pct": int(item.get("slo_target_pct", item.get("target_pct", 0))),
                    "on_time_pct": int(item.get("on_time_pct", item.get("sla_pct", 0))),
                    "open_cases": int(item.get("open_cases", 0)),
                    "at_risk_cases": int(item.get("at_risk_cases", 0)),
                    "status": str(item.get("status", "Unknown")),
                }
            )
        return normalized


sla_service = SLAService()

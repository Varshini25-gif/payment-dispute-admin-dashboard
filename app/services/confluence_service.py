"""
Confluence publication service module.
Fetches and normalizes Confluence publication history data with local fallback.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any

import pandas as pd

from app.services.api_client import APIClient

logger = logging.getLogger(__name__)


class ConfluenceService(APIClient):
    """Service for Confluence publication logs and status analytics."""

    def get_publication_logs(self, filters: dict[str, Any] | None = None) -> pd.DataFrame:
        """
        Return normalized publication logs as a DataFrame.

        Falls back to deterministic sample data when API is unavailable.
        """
        params = self._build_query_params(filters or {})

        try:
            payload = self.get("/confluence/publications", params=params)
            return self._normalize_logs_payload(payload)
        except Exception as exc:
            logger.warning("Falling back to sample Confluence logs: %s", exc)
            sample = self._generate_sample_publications(120)
            return self._filter_dataframe(sample, filters or {})

    def get_publication_summary(self, filters: dict[str, Any] | None = None) -> dict[str, Any]:
        """Return summary metrics for the current filters."""
        filters = filters or {}

        try:
            payload = self.get("/confluence/publications/summary", params=self._build_query_params(filters))
            summary = payload or {}
            return {
                "total": int(summary.get("total", 0)),
                "success": int(summary.get("success", 0)),
                "failed": int(summary.get("failed", 0)),
                "in_progress": int(summary.get("in_progress", 0)),
                "partial": int(summary.get("partial", 0)),
                "is_fallback": False,
            }
        except Exception:
            frame = self.get_publication_logs(filters)
            if frame.empty:
                return {
                    "total": 0,
                    "success": 0,
                    "failed": 0,
                    "in_progress": 0,
                    "partial": 0,
                    "is_fallback": True,
                }

            status_counts = frame["Publish Status"].value_counts()
            return {
                "total": int(len(frame)),
                "success": int(status_counts.get("Published", 0)),
                "failed": int(status_counts.get("Failed", 0)),
                "in_progress": int(status_counts.get("In Progress", 0)),
                "partial": int(status_counts.get("Partial", 0)),
                "is_fallback": True,
            }

    def get_distinct_spaces(self) -> list[str]:
        """Return available Confluence space keys."""
        try:
            payload = self.get("/confluence/spaces")
            if isinstance(payload, dict):
                payload = payload.get("items", [])
            keys = sorted(
                {
                    str(item.get("key", "")).strip().upper()
                    for item in (payload or [])
                    if str(item.get("key", "")).strip()
                }
            )
            return ["All"] + keys
        except Exception:
            frame = self._generate_sample_publications(40)
            keys = sorted(frame["Space Key"].dropna().astype(str).unique().tolist())
            return ["All"] + keys

    def get_distinct_publishers(self) -> list[str]:
        """Return list of users who triggered publication events."""
        try:
            payload = self.get("/confluence/publications/publishers")
            if isinstance(payload, dict):
                payload = payload.get("items", [])
            publishers = sorted(
                {
                    str(item.get("name", item.get("email", ""))).strip()
                    for item in (payload or [])
                    if str(item.get("name", item.get("email", ""))).strip()
                }
            )
            return ["All"] + publishers
        except Exception:
            frame = self._generate_sample_publications(40)
            values = sorted(frame["Published By"].dropna().astype(str).unique().tolist())
            return ["All"] + values

    def _build_query_params(self, filters: dict[str, Any]) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if filters.get("search_query"):
            params["q"] = filters["search_query"]
        if filters.get("status") and filters["status"] != "All":
            params["status"] = filters["status"]
        if filters.get("space_key") and filters["space_key"] != "All":
            params["space"] = filters["space_key"]
        if filters.get("published_by") and filters["published_by"] != "All":
            params["published_by"] = filters["published_by"]

        start_date = filters.get("start_date")
        end_date = filters.get("end_date")
        if start_date:
            params["start_date"] = str(start_date)
        if end_date:
            params["end_date"] = str(end_date)
        return params

    def _normalize_logs_payload(self, payload: Any) -> pd.DataFrame:
        if isinstance(payload, dict):
            items = payload.get("items", [])
        else:
            items = payload or []

        rows: list[dict[str, Any]] = []
        for item in items:
            published_at = self._coerce_datetime(
                item.get("published_at")
                or item.get("publication_timestamp")
                or item.get("created_at")
            )
            rows.append(
                {
                    "Publication ID": str(item.get("publication_id", item.get("id", ""))),
                    "Page Title": str(item.get("page_title", item.get("title", "Untitled"))),
                    "Space Key": str(item.get("space_key", item.get("space", "UNKNOWN"))).upper(),
                    "Page Link": str(item.get("page_link", item.get("url", ""))),
                    "Publish Status": self._normalize_status(item.get("status", "Unknown")),
                    "Published By": str(item.get("published_by", item.get("actor", "Unknown"))),
                    "Published At": published_at,
                    "Published At Display": published_at.strftime("%Y-%m-%d %H:%M:%S") if published_at else "",
                    "Error Message": str(item.get("error_message", "")),
                }
            )

        frame = pd.DataFrame(rows)
        if frame.empty:
            return pd.DataFrame(
                columns=[
                    "Publication ID",
                    "Page Title",
                    "Space Key",
                    "Page Link",
                    "Publish Status",
                    "Published By",
                    "Published At",
                    "Published At Display",
                    "Error Message",
                ]
            )

        return frame.sort_values(by="Published At", ascending=False).reset_index(drop=True)

    def _filter_dataframe(self, frame: pd.DataFrame, filters: dict[str, Any]) -> pd.DataFrame:
        filtered = frame.copy()

        search_query = str(filters.get("search_query", "")).strip().lower()
        if search_query:
            filtered["_search"] = filtered.apply(
                lambda row: " ".join(
                    [
                        str(row.get("Publication ID", "")).lower(),
                        str(row.get("Page Title", "")).lower(),
                        str(row.get("Space Key", "")).lower(),
                        str(row.get("Published By", "")).lower(),
                        str(row.get("Publish Status", "")).lower(),
                    ]
                ),
                axis=1,
            )
            filtered = filtered[filtered["_search"].str.contains(search_query, na=False)].copy()
            filtered = filtered.drop(columns=["_search"])

        status = filters.get("status", "All")
        if status and status != "All":
            filtered = filtered[filtered["Publish Status"] == status]

        space_key = filters.get("space_key", "All")
        if space_key and space_key != "All":
            filtered = filtered[filtered["Space Key"] == str(space_key).upper()]

        published_by = filters.get("published_by", "All")
        if published_by and published_by != "All":
            filtered = filtered[filtered["Published By"] == published_by]

        start_date = filters.get("start_date")
        if start_date is not None:
            filtered = filtered[filtered["Published At"].dt.date >= start_date]

        end_date = filters.get("end_date")
        if end_date is not None:
            filtered = filtered[filtered["Published At"].dt.date <= end_date]

        return filtered.sort_values(by="Published At", ascending=False).reset_index(drop=True)

    def _generate_sample_publications(self, count: int = 100) -> pd.DataFrame:
        statuses = ["Published", "Failed", "In Progress", "Partial"]
        spaces = ["PAY", "OPS", "RISK", "FIN", "SUP"]
        publishers = [
            "alex.rivera@example.com",
            "jordan.lee@example.com",
            "morgan.kim@example.com",
            "system-bot",
        ]

        now = datetime.now().replace(microsecond=0)
        rows: list[dict[str, Any]] = []
        for index in range(count):
            status = statuses[index % len(statuses)]
            published_at = now - timedelta(hours=index * 3)
            page_id = 24000 + index
            title = f"Dispute Runbook {index % 15 + 1}"
            space = spaces[index % len(spaces)]
            publisher = publishers[index % len(publishers)]
            rows.append(
                {
                    "Publication ID": f"PUB-{120000 + index}",
                    "Page Title": title,
                    "Space Key": space,
                    "Page Link": f"https://confluence.example.com/wiki/spaces/{space}/pages/{page_id}",
                    "Publish Status": status,
                    "Published By": publisher,
                    "Published At": published_at,
                    "Published At Display": published_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "Error Message": "Publish webhook timeout" if status == "Failed" else "",
                }
            )

        frame = pd.DataFrame(rows)
        return frame.sort_values(by="Published At", ascending=False).reset_index(drop=True)

    def _coerce_datetime(self, value: Any) -> datetime | None:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        try:
            text = str(value).replace("Z", "+00:00")
            return datetime.fromisoformat(text).replace(tzinfo=None)
        except ValueError:
            return None

    def _normalize_status(self, value: Any) -> str:
        normalized = str(value or "").strip().lower().replace("-", " ").replace("_", " ")
        if normalized in {"success", "published", "completed"}:
            return "Published"
        if normalized in {"failed", "error", "errored"}:
            return "Failed"
        if normalized in {"in progress", "processing", "running"}:
            return "In Progress"
        if normalized in {"partial", "partially published"}:
            return "Partial"
        return "Unknown"


confluence_service = ConfluenceService()

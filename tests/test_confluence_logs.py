from datetime import datetime

import pandas as pd

from app.components.publication_filters import apply_publication_filters
from app.components.status_badges import normalize_publish_status
from app.pages.confluence_logs import summarize_publication_history


def _build_publication_frame() -> pd.DataFrame:
    rows = [
        {
            "Publication ID": "PUB-1",
            "Page Title": "Runbook A",
            "Space Key": "OPS",
            "Page Link": "https://confluence.example.com/wiki/OPS/A",
            "Publish Status": "Published",
            "Published By": "alex@example.com",
            "Published At": datetime(2026, 6, 24, 8, 0, 0),
            "Published At Display": "2026-06-24 08:00:00",
            "Error Message": "",
        },
        {
            "Publication ID": "PUB-2",
            "Page Title": "Runbook B",
            "Space Key": "RISK",
            "Page Link": "https://confluence.example.com/wiki/RISK/B",
            "Publish Status": "Failed",
            "Published By": "sam@example.com",
            "Published At": datetime(2026, 6, 23, 8, 0, 0),
            "Published At Display": "2026-06-23 08:00:00",
            "Error Message": "Timeout",
        },
        {
            "Publication ID": "PUB-3",
            "Page Title": "Runbook C",
            "Space Key": "OPS",
            "Page Link": "https://confluence.example.com/wiki/OPS/C",
            "Publish Status": "In Progress",
            "Published By": "alex@example.com",
            "Published At": datetime(2026, 6, 22, 8, 0, 0),
            "Published At Display": "2026-06-22 08:00:00",
            "Error Message": "",
        },
    ]
    return pd.DataFrame(rows)


def test_normalize_publish_status_maps_common_aliases():
    assert normalize_publish_status("success") == "Published"
    assert normalize_publish_status("errored") == "Failed"
    assert normalize_publish_status("in_progress") == "In Progress"
    assert normalize_publish_status("partially-published") == "Partial"


def test_apply_publication_filters_search_and_status():
    frame = _build_publication_frame()
    filtered = apply_publication_filters(
        frame,
        {
            "search_query": "runbook",
            "status": "Failed",
            "space_key": "All",
            "published_by": "All",
            "start_date": None,
            "end_date": None,
        },
    )

    assert len(filtered) == 1
    assert filtered.iloc[0]["Publication ID"] == "PUB-2"


def test_summarize_publication_history_counts_statuses():
    frame = _build_publication_frame()
    summary = summarize_publication_history(frame)

    assert summary["total"] == 3
    assert summary["published"] == 1
    assert summary["failed"] == 1
    assert summary["in_progress"] == 1
    assert summary["partial"] == 0

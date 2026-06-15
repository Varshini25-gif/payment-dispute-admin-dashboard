import pandas as pd

from app.pages.jira_tracking import filter_issues, summarize_issues


def test_filter_issues_applies_search_status_and_priority():
    issues = pd.DataFrame(
        [
            {
                "Issue Key": "JIRA-101",
                "Summary": "Chargeback review",
                "Status": "In Progress",
                "Priority": "High",
                "Assignee": "Jordan",
                "Linked Disputes": "DIS-1001, DIS-1002",
            },
            {
                "Issue Key": "JIRA-102",
                "Summary": "Refund mismatch",
                "Status": "Done",
                "Priority": "Low",
                "Assignee": "Taylor",
                "Linked Disputes": "DIS-1003",
            },
        ]
    )

    filtered = filter_issues(issues, search_term="chargeback", status="In Progress", priority="High")

    assert len(filtered) == 1
    assert filtered.iloc[0]["Issue Key"] == "JIRA-101"
    assert filtered.iloc[0]["Status"] == "In Progress"


def test_summarize_issues_counts_statuses_and_linked_disputes():
    issues = pd.DataFrame(
        [
            {"Issue Key": "JIRA-101", "Status": "In Progress", "Linked Disputes": "DIS-1001, DIS-1002"},
            {"Issue Key": "JIRA-102", "Status": "Done", "Linked Disputes": "DIS-1003"},
            {"Issue Key": "JIRA-103", "Status": "To Do", "Linked Disputes": ""},
        ]
    )

    summary = summarize_issues(issues)

    assert summary["total_issues"] == 3
    assert summary["open_issues"] == 2
    assert summary["linked_disputes"] == 3
    assert summary["status_breakdown"]["In Progress"] == 1

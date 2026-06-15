import pandas as pd
import streamlit as st


def generate_sample_issues(count=8):
    """Generate deterministic Jira issues for the tracking view."""
    statuses = ["To Do", "In Progress", "In Review", "Done"]
    priorities = ["High", "Medium", "Low"]
    assignees = ["Jordan", "Taylor", "Morgan", "Casey", "Riley"]
    summaries = [
        "Review chargeback backlog for Acme Corp",
        "Verify refund mismatch for Globex",
        "Investigate duplicate charge alert",
        "Escalate high-value dispute for Stark Industries",
        "Confirm payment reroute for Initech",
        "Update SLA risk notes for Hooli",
        "Close fraud review for Umbrella Corp",
        "Prepare agent handoff for Dunder Mifflin",
    ]

    rows = []
    for index in range(count):
        linked_disputes = [f"DIS-{1000 + index * 2:04d}", f"DIS-{1001 + index * 2:04d}"]
        if index % 3 == 0:
            linked_disputes = [linked_disputes[0]]
        rows.append(
            {
                "Issue Key": f"JIRA-{100 + index:03d}",
                "Summary": summaries[index % len(summaries)],
                "Status": statuses[index % len(statuses)],
                "Priority": priorities[index % len(priorities)],
                "Assignee": assignees[index % len(assignees)],
                "Linked Disputes": ", ".join(linked_disputes),
                "Updated": f"2026-06-{(15 + index) % 28 + 1:02d}",
            }
        )

    return pd.DataFrame(rows)


def filter_issues(data, search_term="", status="All", priority="All"):
    """Filter Jira issues by text search, status, and priority."""
    filtered = data.copy()

    search_term = (search_term or "").strip().lower()
    if search_term:
        filtered["_jira_search"] = filtered.apply(
            lambda row: " ".join(
                str(value).lower()
                for value in [
                    row.get("Issue Key"),
                    row.get("Summary"),
                    row.get("Assignee"),
                    row.get("Linked Disputes"),
                ]
            ),
            axis=1,
        )
        filtered = filtered[filtered["_jira_search"].str.contains(search_term, na=False)].copy()
        filtered = filtered.drop(columns=["_jira_search"])

    if status and status != "All":
        filtered = filtered[filtered["Status"] == status]

    if priority and priority != "All":
        filtered = filtered[filtered["Priority"] == priority]

    return filtered.reset_index(drop=True)


def summarize_issues(data):
    """Return summary metrics for the Jira issue set."""
    issues = data.copy()
    if issues.empty:
        return {
            "total_issues": 0,
            "open_issues": 0,
            "linked_disputes": 0,
            "status_breakdown": {},
        }

    status_values = issues["Status"].fillna("Unknown").astype(str)
    status_breakdown = status_values.value_counts().to_dict()

    open_issues = int(status_values[~status_values.isin(["Done", "Closed", "Resolved"])].shape[0])

    linked_disputes = 0
    for raw_value in issues["Linked Disputes"].fillna("").astype(str):
        linked_disputes += sum(1 for entry in raw_value.split(",") if entry.strip())

    return {
        "total_issues": int(len(issues)),
        "open_issues": open_issues,
        "linked_disputes": linked_disputes,
        "status_breakdown": dict(sorted(status_breakdown.items())),
    }


def render():
    """Render the Jira tracking page."""
    st.header("🧾 Jira Tracking")
    st.markdown("Track Jira issues, apply filters, and review the disputes linked to each item.")

    issues = generate_sample_issues(10)

    search_term = st.text_input(
        "Search issues",
        placeholder="Search by issue key, summary, assignee, or linked dispute",
        key="jira_search",
    )

    status_filter = st.selectbox(
        "Status",
        ["All", *sorted(issues["Status"].dropna().unique().tolist())],
        key="jira_status",
    )
    priority_filter = st.selectbox(
        "Priority",
        ["All", *sorted(issues["Priority"].dropna().unique().tolist())],
        key="jira_priority",
    )

    filtered_issues = filter_issues(issues, search_term=search_term, status=status_filter, priority=priority_filter)
    summary = summarize_issues(filtered_issues)

    metric_cols = st.columns(4)
    with metric_cols[0]:
        st.metric("Total issues", summary["total_issues"])
    with metric_cols[1]:
        st.metric("Open issues", summary["open_issues"])
    with metric_cols[2]:
        st.metric("Linked disputes", summary["linked_disputes"])
    with metric_cols[3]:
        st.metric("Status groups", len(summary["status_breakdown"]))

    st.markdown("---")

    status_cols = st.columns(2)
    with status_cols[0]:
        st.subheader("Issue Status Overview")
        status_breakdown = summary.get("status_breakdown", {})
        if status_breakdown:
            for status_name, count in status_breakdown.items():
                st.progress(count / max(summary["total_issues"], 1), text=f"{status_name}: {count}")
        else:
            st.info("No issues match the current filters.")

    with status_cols[1]:
        st.subheader("Linked Disputes")
        if filtered_issues.empty:
            st.info("No linked disputes are available for the current issue filters.")
        else:
            for _, row in filtered_issues.iterrows():
                linked = [item.strip() for item in str(row.get("Linked Disputes", "")).split(",") if item.strip()]
                if linked:
                    st.markdown(f"- **{row['Issue Key']}** — {', '.join(linked)}")
                else:
                    st.markdown(f"- **{row['Issue Key']}** — No linked disputes")

    st.markdown("---")
    st.subheader("Jira Issues")
    display_frame = filtered_issues.copy()
    display_frame = display_frame[["Issue Key", "Summary", "Status", "Priority", "Assignee", "Linked Disputes", "Updated"]]
    st.dataframe(display_frame, use_container_width=True, hide_index=True)

    st.caption("Issue filters update the table and the linked-dispute summary in real time.")

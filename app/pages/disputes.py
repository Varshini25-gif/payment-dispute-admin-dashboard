import math

import pandas as pd
import streamlit as st

from app.components.common import render_priority_badge, render_status_badge
from app.components.tables import filter_disputes, generate_sample_disputes, paginate_dataframe
from app.state.session import SessionState


def render():
    SessionState.initialize()

    st.header("💬 Disputes")
    st.markdown("Manage incoming disputes, review case details, and assign follow-up tasks.")

    disputes_data = SessionState.get_disputes_data()
    if not isinstance(disputes_data, pd.DataFrame):
        disputes_data = generate_sample_disputes(25)
        SessionState.set_disputes_data(disputes_data)
    else:
        disputes_data = disputes_data.copy()

    search_term = st.text_input(
        "Search disputes",
        key="disputes_search",
        placeholder="Search by dispute ID, customer, reason, or assignee",
    )

    status_filter = st.selectbox(
        "Status",
        ["All", "Pending", "In Review", "Resolved", "Rejected"],
        key="disputes_status",
    )

    priority_filter = st.selectbox(
        "Priority",
        ["All", "Low", "Medium", "High"],
        key="disputes_priority",
    )

    page_size = st.selectbox(
        "Rows per page",
        [5, 10, 20],
        index=1,
        key="disputes_page_size",
    )
    page_size = int(page_size)

    filtered_disputes = filter_disputes(
        disputes_data,
        search_term=search_term,
        status=status_filter,
        priority=priority_filter,
    )
    SessionState.set_dispute_filter({
        "search_term": search_term,
        "status": status_filter,
        "priority": priority_filter,
    })

    if "disputes_page" not in st.session_state:
        st.session_state["disputes_page"] = 1

    total_pages = max(1, math.ceil(len(filtered_disputes) / page_size)) if filtered_disputes else 1
    if st.session_state["disputes_page"] > total_pages:
        st.session_state["disputes_page"] = total_pages

    page_index = st.session_state["disputes_page"]
    page_disputes, pagination = paginate_dataframe(
        filtered_disputes,
        page_index=page_index,
        page_size=page_size,
    )
    st.session_state["disputes_page"] = pagination["page_index"]

    summary_cols = st.columns(3)
    with summary_cols[0]:
        st.metric("Matching disputes", len(filtered_disputes))
    with summary_cols[1]:
        st.metric("Current page", pagination["page_index"])
    with summary_cols[2]:
        st.metric("Total pages", pagination["total_pages"])

    display_df = page_disputes.copy()
    display_df["Status"] = display_df["Status"].apply(render_status_badge)
    display_df["Priority"] = display_df["Priority"].apply(render_priority_badge)
    display_df = display_df[
        [
            "Dispute ID",
            "Customer",
            "Amount",
            "Status",
            "Priority",
            "Created",
            "Reason",
            "Assigned To",
        ]
    ]

    st.dataframe(display_df, use_container_width=True, hide_index=True)

    st.caption(
        f"Showing {len(page_disputes)} of {len(filtered_disputes)} disputes."
    )

    nav_cols = st.columns([1, 1, 1])
    with nav_cols[0]:
        if st.button("← Previous", disabled=not pagination["has_prev"], key="disputes_prev"):
            st.session_state["disputes_page"] = max(1, pagination["page_index"] - 1)
    with nav_cols[1]:
        st.markdown(f"**Page {pagination['page_index']} of {pagination['total_pages']}**")
    with nav_cols[2]:
        if st.button("Next →", disabled=not pagination["has_next"], key="disputes_next"):
            st.session_state["disputes_page"] = min(pagination["total_pages"], pagination["page_index"] + 1)

    st.markdown("---")

    with st.expander("Dispute Details Drawer", expanded=True):
        if filtered_disputes.empty:
            st.info("No disputes match the current filters.")
        else:
            selected_dispute_id = st.selectbox(
                "Open dispute details",
                filtered_disputes["Dispute ID"].tolist(),
                key="selected_dispute_id",
            )
            selected_dispute = filtered_disputes.loc[
                filtered_disputes["Dispute ID"] == selected_dispute_id
            ].iloc[0]

            st.markdown(f"### {selected_dispute['Dispute ID']} — {selected_dispute['Customer']}")

            detail_cols = st.columns(2)
            with detail_cols[0]:
                st.markdown(f"**Status:** {render_status_badge(selected_dispute['Status'])}")
                st.markdown(f"**Priority:** {render_priority_badge(selected_dispute['Priority'])}")
                st.markdown(f"**Amount:** {selected_dispute['Amount']}")
            with detail_cols[1]:
                st.markdown(f"**Created:** {selected_dispute['Created']}")
                st.markdown(f"**Assigned To:** {selected_dispute['Assigned To']}")

            st.markdown("**Reason**")
            st.write(selected_dispute["Reason"])


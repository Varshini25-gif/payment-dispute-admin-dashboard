import math
from datetime import datetime

import pandas as pd
import streamlit as st

from app.components.advanced_filters import (
    apply_advanced_dispute_filters,
    build_filter_query_params,
    get_default_dispute_filters,
    render_advanced_dispute_filters,
)
from app.components.common import render_priority_badge, render_status_badge
from app.components.export_buttons import render_csv_export_button
from app.components.filter_drawer import render_filter_drawer
from app.components.tables import generate_sample_disputes, paginate_dataframe
from app.services import dispute_service
from app.state.session import SessionState


REQUIRED_DISPUTE_COLUMNS = [
    "Dispute ID",
    "Customer",
    "Amount",
    "Status",
    "Priority",
    "Created",
    "Reason",
    "Assigned To",
]


def _derive_dispute_type(reason: str) -> str:
    reason_text = str(reason).lower()
    if "fraud" in reason_text or "unauthorized" in reason_text:
        return "Fraud"
    if "refund" in reason_text:
        return "Refund"
    if "duplicate" in reason_text or "charge" in reason_text:
        return "Chargeback"
    return "General"


def _derive_queue(assignee: str) -> str:
    queue_map = {
        "Jordan": "Chargeback Queue",
        "Taylor": "Operations Queue",
        "Morgan": "Risk Queue",
        "Casey": "Escalations Queue",
        "Riley": "Refund Queue",
    }
    return queue_map.get(str(assignee), "General Queue")


def _derive_sla_bucket(status: str, priority: str, created_value) -> str:
    status_text = str(status)
    if status_text == "Resolved":
        return "Met"

    created_ts = pd.to_datetime(created_value, errors="coerce")
    if pd.notna(created_ts):
        age_days = (datetime.now().date() - created_ts.date()).days
    else:
        age_days = 0

    if str(priority) == "High" and age_days >= 2:
        return "Breach Risk"
    if age_days >= 7:
        return "Breached"
    return "On Track"


def _enrich_dispute_dimensions(df: pd.DataFrame) -> pd.DataFrame:
    enriched = df.copy()

    if "Queue" not in enriched.columns:
        enriched["Queue"] = enriched["Assigned To"].apply(_derive_queue)

    if "Dispute Type" not in enriched.columns:
        enriched["Dispute Type"] = enriched["Reason"].apply(_derive_dispute_type)

    if "SLA Bucket" not in enriched.columns:
        enriched["SLA Bucket"] = enriched.apply(
            lambda row: _derive_sla_bucket(
                row.get("Status"),
                row.get("Priority"),
                row.get("Created"),
            ),
            axis=1,
        )

    return enriched


def _normalize_dispute_records(records):
    if records is None:
        return pd.DataFrame(columns=REQUIRED_DISPUTE_COLUMNS)

    if isinstance(records, dict) and "data" in records:
        records = records["data"]

    if not isinstance(records, list):
        raise ValueError("Unexpected dispute API response format")

    if len(records) == 0:
        return pd.DataFrame(columns=REQUIRED_DISPUTE_COLUMNS)

    df = pd.DataFrame(records)
    rename_map = {
        "dispute_id": "Dispute ID",
        "id": "Dispute ID",
        "customer": "Customer",
        "customer_name": "Customer",
        "amount": "Amount",
        "status": "Status",
        "priority": "Priority",
        "queue": "Queue",
        "queue_name": "Queue",
        "sla": "SLA Bucket",
        "sla_bucket": "SLA Bucket",
        "dispute_type": "Dispute Type",
        "type": "Dispute Type",
        "created": "Created",
        "created_date": "Created",
        "reason": "Reason",
        "assigned_to": "Assigned To",
        "assignee": "Assigned To",
    }
    df = df.rename(columns=rename_map)

    missing_columns = [col for col in REQUIRED_DISPUTE_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(
            f"Dispute API response is missing required fields: {', '.join(missing_columns)}"
        )

    if pd.api.types.is_numeric_dtype(df["Amount"]):
        df["Amount"] = df["Amount"].apply(lambda value: f"${value:,.2f}")

    return _enrich_dispute_dimensions(df)


def render():
    SessionState.initialize()

    st.header("💬 Disputes")
    st.markdown("Manage incoming disputes, review case details, and assign follow-up tasks.")

    if "disputes_page" not in st.session_state:
        st.session_state["disputes_page"] = 1

    refresh_requested = st.button("Refresh disputes", key="refresh_disputes")

    saved_filters = SessionState.get_dispute_filter()
    default_filters = get_default_dispute_filters(saved_filters)

    cached_data = SessionState.get_disputes_data()
    if isinstance(cached_data, pd.DataFrame):
        cached_data = _enrich_dispute_dimensions(cached_data)
        queue_options = ["All"] + sorted(cached_data["Queue"].dropna().astype(str).unique().tolist())
        sla_options = ["All"] + sorted(cached_data["SLA Bucket"].dropna().astype(str).unique().tolist())
        dispute_type_options = ["All"] + sorted(cached_data["Dispute Type"].dropna().astype(str).unique().tolist())
    else:
        queue_options = ["All", "Chargeback Queue", "Operations Queue", "Risk Queue", "Escalations Queue", "Refund Queue", "General Queue"]
        sla_options = ["All", "On Track", "Breach Risk", "Breached", "Met"]
        dispute_type_options = ["All", "Chargeback", "Fraud", "Refund", "General"]

    with render_filter_drawer("Dispute Filters", expanded=True):
        active_filters, apply_requested = render_advanced_dispute_filters(
            queue_options=queue_options,
            sla_options=sla_options,
            dispute_type_options=dispute_type_options,
            defaults=default_filters,
            form_key="dispute_filter_drawer_form",
        )

    if apply_requested:
        st.session_state["disputes_page"] = 1

    disputes_data = cached_data
    if refresh_requested or apply_requested or not isinstance(disputes_data, pd.DataFrame):
        with st.spinner("Loading disputes from API..."):
            try:
                query_params = build_filter_query_params(active_filters, limit=100)
                api_response = dispute_service.get_disputes(**query_params)
                disputes_data = _normalize_dispute_records(api_response)
                SessionState.set_disputes_data(disputes_data)
                st.success("Disputes loaded successfully.")
            except Exception as exc:
                st.error(f"Unable to load disputes: {exc}")
                if not isinstance(disputes_data, pd.DataFrame):
                    disputes_data = _enrich_dispute_dimensions(generate_sample_disputes(25))
                    SessionState.set_disputes_data(disputes_data)
                    st.warning("Showing fallback sample disputes while the API is unavailable.")

    if not isinstance(disputes_data, pd.DataFrame):
        disputes_data = _enrich_dispute_dimensions(generate_sample_disputes(25))
        SessionState.set_disputes_data(disputes_data)
    else:
        disputes_data = _enrich_dispute_dimensions(disputes_data.copy())

    page_size = st.selectbox(
        "Rows per page",
        [5, 10, 20],
        index=1,
        key="disputes_page_size",
    )
    page_size = int(page_size)

    filtered_disputes = apply_advanced_dispute_filters(disputes_data, active_filters)
    SessionState.set_dispute_filter(active_filters)

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

    export_col, summary_col = st.columns([1, 4])
    with export_col:
        render_csv_export_button(
            filtered_disputes,
            file_prefix="disputes",
            label="⬇️ Export CSV",
            key="disputes_csv_export_button",
        )
    with summary_col:
        st.caption("Export includes all rows matching current filters, not only this page.")

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
            "Queue",
            "SLA Bucket",
            "Dispute Type",
            "Created",
            "Reason",
            "Assigned To",
        ]
    ]

    st.dataframe(display_df, use_container_width=True, hide_index=True)

    st.caption(f"Showing {len(page_disputes)} of {len(filtered_disputes)} disputes.")

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
                st.markdown(f"**Queue:** {selected_dispute['Queue']}")
            with detail_cols[1]:
                st.markdown(f"**Created:** {selected_dispute['Created']}")
                st.markdown(f"**Assigned To:** {selected_dispute['Assigned To']}")
                st.markdown(f"**SLA:** {selected_dispute['SLA Bucket']}")
                st.markdown(f"**Dispute Type:** {selected_dispute['Dispute Type']}")

            st.markdown("**Reason**")
            st.write(selected_dispute["Reason"])

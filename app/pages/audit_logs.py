"""
Audit Logs page
Full-featured audit trail: filters, searchable table, activity timeline, export.
"""

from datetime import datetime, timedelta, date
import streamlit as st

from app.services.audit_service import (
    get_audit_logs,
    get_paginated_logs,
    get_summary,
    get_distinct_dispute_ids,
    get_distinct_actors,
    get_distinct_actions,
    get_recent_activity,
    export_to_csv,
)
from app.components.audit_table import render_audit_table
from app.components.activity_timeline import (
    render_activity_timeline,
    render_activity_summary_badges,
)


# ─────────────────────────────────────────────────────────────────────────────
# Page config (only called here when this file IS the entry-point)
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    st.set_page_config(
        page_title="Audit Logs | Admin Dashboard",
        page_icon="📋",
        layout="wide",
    )


def render_audit_logs_page() -> None:
    """Main render function – call this from main.py or use as standalone page."""

    # ── Page header ───────────────────────────────────────────────────────────
    st.title("📋 Audit Logs")
    st.markdown(
        "Complete audit trail of all system and user actions across disputes. "
        "Use the filters below to narrow results, then export as CSV."
    )
    st.divider()

    # ── Summary KPI badges ────────────────────────────────────────────────────
    summary = get_summary()
    render_activity_summary_badges(summary)
    st.markdown("")

    # ── Sidebar / filter panel ────────────────────────────────────────────────
    with st.expander("🔍 Filters", expanded=True):
        f_col1, f_col2, f_col3, f_col4 = st.columns([2, 2, 2, 2])

        with f_col1:
            st.markdown("**Date range**")
            preset = st.radio(
                "Preset",
                ["Last 7 days", "Last 30 days", "Last 90 days", "Custom"],
                horizontal=True,
                label_visibility="collapsed",
                key="audit_preset",
            )
            today = date.today()
            if preset == "Last 7 days":
                default_start, default_end = today - timedelta(days=7), today
            elif preset == "Last 30 days":
                default_start, default_end = today - timedelta(days=30), today
            elif preset == "Last 90 days":
                default_start, default_end = today - timedelta(days=90), today
            else:
                default_start, default_end = today - timedelta(days=30), today

            if preset == "Custom":
                start_date = st.date_input("From", value=default_start, key="audit_start")
                end_date = st.date_input("To",   value=default_end,   key="audit_end")
            else:
                start_date, end_date = default_start, default_end
                st.caption(f"{start_date} → {end_date}")

        with f_col2:
            dispute_id = st.selectbox(
                "Dispute ID",
                get_distinct_dispute_ids(),
                key="audit_dispute_id",
            )
            action_filter = st.selectbox(
                "Action",
                get_distinct_actions(),
                key="audit_action",
            )

        with f_col3:
            status_filter = st.selectbox(
                "Status",
                ["All", "Success", "Warning", "Failure", "Info"],
                key="audit_status",
            )
            actor_filter = st.selectbox(
                "Actor / Agent",
                get_distinct_actors(),
                key="audit_actor",
            )

        with f_col4:
            st.markdown("**Keyword search**")
            search_query = st.text_input(
                "Search",
                placeholder="Log ID, action, actor, dispute…",
                label_visibility="collapsed",
                key="audit_search_query",
            )
            st.markdown("**Quick filters**")
            qf_cols = st.columns(2)
            with qf_cols[0]:
                if st.button("❌ Failures only", use_container_width=True, key="qf_fail"):
                    st.session_state["audit_status"] = "Failure"
                    st.rerun()
            with qf_cols[1]:
                if st.button("⚠️ Warnings only", use_container_width=True, key="qf_warn"):
                    st.session_state["audit_status"] = "Warning"
                    st.rerun()

    # ── Fetch filtered data ───────────────────────────────────────────────────
    filtered_df = get_audit_logs(
        search_query=search_query,
        dispute_id=dispute_id,
        action_filter=action_filter,
        status_filter=status_filter,
        actor_filter=actor_filter,
        start_date=start_date,
        end_date=end_date,
    )

    # ── Export button ─────────────────────────────────────────────────────────
    export_col, info_col = st.columns([1, 5])
    with export_col:
        st.download_button(
            label="⬇️ Export CSV",
            data=export_to_csv(filtered_df),
            file_name=f"audit_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True,
            key="audit_export_btn",
        )
    with info_col:
        st.caption(f"**{len(filtered_df):,}** records match current filters.")

    st.divider()

    # ── Main layout: table (left) + timeline (right) ──────────────────────────
    table_col, timeline_col = st.columns([3, 1], gap="large")

    with table_col:
        render_audit_table(data=filtered_df, page_key="audit_main_page")

    with timeline_col:
        recent = get_recent_activity(limit=12)
        render_activity_timeline(recent, title="Latest Activity")


# ── Entry-point when run directly ─────────────────────────────────────────────
if __name__ == "__main__":
    render_audit_logs_page()

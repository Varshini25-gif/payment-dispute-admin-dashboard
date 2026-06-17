"""
Audit table component
Displays searchable audit logs table with pagination.
"""

import math
from datetime import datetime, timedelta
import pandas as pd
import streamlit as st


def generate_sample_audit_logs(count=100):
    """Generate deterministic sample audit logs for table rendering."""
    actions = ["Create", "Update", "Delete", "View", "Export", "Status Change", "Assign", "Unassign"]
    statuses = ["Success", "Failure", "Warning"]
    users = ["John Smith", "Sarah Johnson", "Mike Davis", "Emma Wilson", "Alex Brown", "Jessica Lee"]
    entities = ["Dispute", "Payment", "User", "Rule", "Configuration", "Report"]
    
    rows = []
    base_date = datetime.now() - timedelta(days=100)
    
    for index in range(count):
        timestamp = base_date + timedelta(hours=index*2)
        rows.append({
            "Log ID": f"LOG-{100000 + index:06d}",
            "Timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "User": users[index % len(users)],
            "Action": actions[index % len(actions)],
            "Entity Type": entities[index % len(entities)],
            "Entity ID": f"{entities[index % len(entities)].upper()}-{1000 + (index % 50):04d}",
            "Status": statuses[index % len(statuses)],
            "Details": f"Modified {['field_1', 'field_2', 'status', 'priority', 'assignment'][index % 5]}",
            "IP Address": f"192.168.{(index // 20) % 256}.{index % 256}",
        })
    
    return pd.DataFrame(rows)


def filter_audit_logs(data, search_term="", action_type=None, status=None, user=None, entity_type=None):
    """Filter audit logs by search text and categorical filters."""
    filtered = data.copy()
    
    # Text search across multiple fields
    search_term = (search_term or "").strip().lower()
    if search_term:
        filtered["_search_index"] = filtered.apply(
            lambda row: " ".join(
                str(value).lower()
                for value in [
                    row.get("Log ID"),
                    row.get("User"),
                    row.get("Action"),
                    row.get("Entity Type"),
                    row.get("Entity ID"),
                    row.get("Details"),
                ]
            ),
            axis=1,
        )
        filtered = filtered[filtered["_search_index"].str.contains(search_term, na=False)].copy()
        filtered = filtered.drop(columns=["_search_index"])
    
    # Category filters
    if action_type and action_type != "All":
        filtered = filtered[filtered["Action"] == action_type]
    
    if status and status != "All":
        filtered = filtered[filtered["Status"] == status]
    
    if user and user != "All":
        filtered = filtered[filtered["User"] == user]
    
    if entity_type and entity_type != "All":
        filtered = filtered[filtered["Entity Type"] == entity_type]
    
    return filtered.reset_index(drop=True)


def paginate_dataframe(data, page_index=1, page_size=10):
    """Return a paginated dataframe slice and pagination metadata."""
    total_rows = len(data)
    page_index = max(1, int(page_index))
    page_size = max(1, int(page_size))
    total_pages = max(1, math.ceil(total_rows / page_size)) if total_rows else 1
    page_index = min(page_index, total_pages)
    
    start_index = (page_index - 1) * page_size
    end_index = start_index + page_size
    page = data.iloc[start_index:end_index].reset_index(drop=True)
    
    return page, {
        "page_index": page_index,
        "page_size": page_size,
        "total_rows": total_rows,
        "total_pages": total_pages,
        "start_index": start_index,
        "end_index": end_index,
        "has_prev": page_index > 1,
        "has_next": page_index < total_pages,
    }


def render_audit_table(data: pd.DataFrame = None, page_key: str = "audit_page"):
    """
    Render searchable audit logs table with pagination.

    Parameters
    ----------
    data : pd.DataFrame, optional
        Pre-filtered data from the service layer.  When None the component
        generates its own sample data so it can still be used standalone.
    page_key : str
        Unique session-state key used for the current page number – allows
        multiple table instances on the same Streamlit page.
    """
    st.subheader("📋 Audit Log Table")

    if page_key not in st.session_state:
        st.session_state[page_key] = 1

    if data is None:
        if "audit_logs_data" not in st.session_state:
            st.session_state.audit_logs_data = generate_sample_audit_logs(100)
        source = st.session_state.audit_logs_data
    else:
        source = data

    # Inline search + column filters
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        search_term = st.text_input(
            "Search logs",
            placeholder="Search by ID, user, action, entity…",
            key="audit_table_search",
        )
    with col2:
        action_opts = ["All"] + sorted(source["Action"].dropna().unique().tolist()) if "Action" in source.columns and len(source) else ["All"]
        action_filter = st.selectbox("Action", action_opts, key="audit_table_action")
    with col3:
        status_opts = ["All"] + sorted(source["Status"].dropna().unique().tolist()) if "Status" in source.columns and len(source) else ["All"]
        status_filter = st.selectbox("Status", status_opts, key="audit_table_status")
    with col4:
        page_size = st.selectbox("Rows / page", [10, 25, 50, 100], key="audit_table_page_size")

    # Reset to page 1 whenever filters change
    filter_sig = (search_term, action_filter, status_filter, page_size)
    if st.session_state.get("_audit_table_last_filter") != filter_sig:
        st.session_state[page_key] = 1
        st.session_state["_audit_table_last_filter"] = filter_sig

    filtered_data = filter_audit_logs(source, search_term=search_term,
                                      action_type=action_filter, status=status_filter)

    page_data, meta = paginate_dataframe(
        filtered_data, page_index=st.session_state[page_key], page_size=page_size
    )

    if len(page_data):
        # Color-code Status column via column_config
        st.dataframe(page_data, use_container_width=True, height=420, hide_index=True)
    else:
        st.info("No audit logs match the current filters.")

    # Pagination bar
    st.markdown("---")
    p_col1, p_col2, p_col3, p_col4, p_col5 = st.columns([1, 1, 1, 1, 1])
    with p_col1:
        if st.button("⬅️ Prev", use_container_width=True, disabled=not meta["has_prev"], key=f"{page_key}_prev"):
            st.session_state[page_key] = meta["page_index"] - 1
            st.rerun()
    with p_col2:
        jump = st.number_input(
            "Page", min_value=1, max_value=meta["total_pages"],
            value=meta["page_index"], key=f"{page_key}_jump", label_visibility="collapsed"
        )
        if jump != meta["page_index"]:
            st.session_state[page_key] = jump
            st.rerun()
    with p_col3:
        st.caption(f"Page **{meta['page_index']}** of **{meta['total_pages']}**")
    with p_col4:
        st.caption(f"Showing **{meta['start_index']+1}–{min(meta['end_index'], meta['total_rows'])}** of **{meta['total_rows']}**")
    with p_col5:
        if st.button("Next ➡️", use_container_width=True, disabled=not meta["has_next"], key=f"{page_key}_next"):
            st.session_state[page_key] = meta["page_index"] + 1
            st.rerun()

    return page_data, filtered_data

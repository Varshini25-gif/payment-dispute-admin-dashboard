"""
Reusable UI Components
"""

import streamlit as st
import pandas as pd


def render_metric_card(label, value, delta=None, icon="📊"):
    """Render a metric card"""
    col1, col2 = st.columns([1, 4])
    with col1:
        st.write(icon)
    with col2:
        st.metric(label, value, delta)


def render_status_badge(status):
    """Render status badge with color"""
    status_colors = {
        "pending": "🟡 Pending",
        "in_review": "🔵 In Review",
        "resolved": "🟢 Resolved",
        "rejected": "🔴 Rejected",
        "active": "🟢 Active",
        "inactive": "🔴 Inactive"
    }
    
    status_lower = status.lower().replace(" ", "_")
    return status_colors.get(status_lower, f"⚪ {status}")


def render_priority_badge(priority):
    """Render priority badge with color"""
    priority_emojis = {
        "low": "🟢 Low",
        "medium": "🟡 Medium",
        "high": "🔴 High"
    }
    
    priority_lower = priority.lower()
    return priority_emojis.get(priority_lower, f"⚪ {priority}")


def render_data_table(data, key=None):
    """Render a data table with styling"""
    if isinstance(data, pd.DataFrame):
        st.dataframe(
            data,
            use_container_width=True,
            hide_index=True,
            key=key
        )
    else:
        st.write(data)


def render_info_box(title, content, icon="ℹ️"):
    """Render an info box"""
    st.info(f"{icon} **{title}**\n\n{content}")


def render_warning_box(title, content, icon="⚠️"):
    """Render a warning box"""
    st.warning(f"{icon} **{title}**\n\n{content}")


def render_error_box(title, content, icon="❌"):
    """Render an error box"""
    st.error(f"{icon} **{title}**\n\n{content}")


def render_success_box(title, content, icon="✅"):
    """Render a success box"""
    st.success(f"{icon} **{title}**\n\n{content}")


def render_column_divider(cols=3):
    """Render column divider"""
    columns = st.columns(cols)
    for col in columns:
        col.write("---")


def render_stats_summary(stats_dict):
    """Render statistics summary with columns"""
    cols = st.columns(len(stats_dict))
    for col, (label, value) in zip(cols, stats_dict.items()):
        with col:
            st.metric(label, value)


def render_expandable_section(title, content_func):
    """Render expandable section with callback"""
    with st.expander(title):
        content_func()


def render_filter_bar(filters_config):
    """Render filter bar with multiple filters"""
    col_widths = [1] * len(filters_config)
    cols = st.columns(col_widths)
    
    filter_values = {}
    for col, (filter_key, filter_config) in zip(cols, filters_config.items()):
        with col:
            filter_type = filter_config.get("type", "text")
            if filter_type == "select":
                filter_values[filter_key] = st.selectbox(
                    filter_config.get("label", filter_key),
                    filter_config.get("options", [])
                )
            elif filter_type == "multiselect":
                filter_values[filter_key] = st.multiselect(
                    filter_config.get("label", filter_key),
                    filter_config.get("options", [])
                )
            else:
                filter_values[filter_key] = st.text_input(
                    filter_config.get("label", filter_key)
                )
    
    return filter_values

import pandas as pd
import streamlit as st

from .common import render_status_badge


def normalize_rule_status(status):
    if status is None:
        return "active"
    text = str(status).strip().lower()
    return "active" if text == "" else text


def build_rule_dataframe(rules, include_inactive=True):
    rows = []
    for rule in rules or []:
        status = normalize_rule_status(rule.get("status", "active"))
        if not include_inactive and status != "active":
            continue

        rows.append({
            "Name": rule.get("name", ""),
            "Condition": rule.get("condition", ""),
            "Priority": rule.get("priority", ""),
            "Destination": rule.get("destination", ""),
            "Status": status,
        })

    return pd.DataFrame(rows)


def get_rule_counts(rules):
    total = len(rules or [])
    active = sum(1 for rule in rules or [] if normalize_rule_status(rule.get("status", "active")) == "active")
    inactive = total - active
    return {
        "total": total,
        "active": active,
        "inactive": inactive,
    }


def render_rule_status_summary(rules):
    counts = get_rule_counts(rules)
    st.subheader("Rule Status Overview")
    col1, col2, col3 = st.columns([1, 1, 1])
    col1.metric("Loaded rules", counts["total"])
    col2.metric("Active rules", counts["active"], delta=f"{counts['active']} active")
    col3.metric("Inactive rules", counts["inactive"], delta=f"{counts['inactive']} inactive")

    if counts["total"]:
        status_labels = sorted({normalize_rule_status(rule.get("status", "active")) for rule in rules})
        status_markup = " • ".join(render_status_badge(status) for status in status_labels)
        st.markdown(f"**Status indicators:** {status_markup}")
    else:
        st.info("No routing rules loaded yet.")


def render_rule_validation_summary(validation_messages):
    if not validation_messages:
        st.success("Routing rules validated successfully. All rules are in good shape.")
        return

    st.subheader("Rule Validation")
    for message in validation_messages:
        if message.get("severity") == "error":
            st.error(message.get("text", "Unknown validation error."))
        elif message.get("severity") == "warning":
            st.warning(message.get("text", "Validation warning."))
        else:
            st.info(message.get("text", "Validation note."))


def render_editable_rule_table(rules, key="editable_routing_rules"):
    st.subheader("Editable Routing Rule Table")
    if not rules:
        st.info("Load YAML rules or paste a valid configuration to edit routing rules here.")
        return rules

    current_table = build_rule_dataframe(rules)
    st.markdown(
        "Edit rule name, condition, priority, destination, and status values inline. "
        "Use `active` or `inactive` for rule status."
    )

    try:
        edited_table = st.data_editor(
            current_table,
            use_container_width=True,
            hide_index=True,
            key=key,
        )
    except AttributeError:
        edited_table = st.experimental_data_editor(
            current_table,
            use_container_width=True,
            num_rows="dynamic",
            key=key,
        )

    if edited_table is None:
        return rules

    edited_table = edited_table.fillna("")
    updated_rules = []
    for row in edited_table.to_dict(orient="records"):
        updated_rules.append({
            "name": str(row.get("Name", "")).strip(),
            "condition": str(row.get("Condition", "")).strip(),
            "priority": str(row.get("Priority", "")).strip().lower(),
            "destination": str(row.get("Destination", "")).strip(),
            "status": normalize_rule_status(row.get("Status", "active")),
        })

    return updated_rules

import streamlit as st
from app.utils.helpers import (
    build_routing_table,
    evaluate_routing_rule,
    match_routing_rules,
    parse_routing_yaml,
    validate_routing_rules,
)

DEFAULT_ROUTING_YAML = """rules:
  - name: High value review
    condition: amount > 1000 and category == "premium"
    priority: high
    destination: Senior Review Team
    status: active

  - name: Low value auto-approve
    condition: amount <= 100 and category == "routine"
    priority: low
    destination: Auto-approve Queue
    status: active

  - name: International escalation
    condition: country == "US" and amount > 500
    priority: medium
    destination: International Routing
    status: active
"""


def render_yaml_upload_section():
    st.subheader("YAML Upload")
    st.write("Upload a YAML routing configuration file or paste YAML content directly.")

    uploaded_file = st.file_uploader(
        "Upload routing rules YAML file",
        type=["yaml", "yml"],
        key="routing_rules_yaml_upload"
    )

    if uploaded_file is not None:
        try:
            uploaded_text = uploaded_file.read().decode("utf-8")
            st.session_state["routing_rules_yaml"] = uploaded_text
        except Exception:
            st.error("Unable to read the uploaded YAML file. Please check the file format.")

    if "routing_rules_yaml" not in st.session_state:
        st.session_state["routing_rules_yaml"] = DEFAULT_ROUTING_YAML

    yaml_content = st.text_area(
        "Routing rules YAML content",
        value=st.session_state["routing_rules_yaml"],
        height=260,
        key="routing_rules_yaml"
    )

    rules, parse_errors = parse_routing_yaml(yaml_content)
    validation_messages = validate_routing_rules(rules)

    if parse_errors:
        for error in parse_errors:
            st.error(error)

    if validation_messages:
        for message in validation_messages:
            if message["severity"] == "error":
                st.error(message["text"])
            else:
                st.warning(message["text"])

    if not rules and not parse_errors:
        st.info("No routing rules found. Paste a YAML configuration or upload a valid file to see rules here.")

    return rules


def render_routing_rule_table(rules):
    st.subheader("Routing Rule Table")

    if not rules:
        st.info("Load or paste routing YAML to populate the rule table.")
        return

    table_data = build_routing_table(rules)
    st.dataframe(table_data, use_container_width=True, hide_index=True)


def render_test_routing_form(rules):
    st.subheader("Test Routing")
    st.write("Enter a sample transaction and see which routing rule would apply.")

    with st.form(key="routing_rule_test_form"):
        amount = st.number_input(
            "Transaction amount",
            min_value=0.0,
            value=250.0,
            step=10.0,
            format="%.2f",
            key="routing_test_amount"
        )
        country = st.text_input("Customer country", value="US", key="routing_test_country")
        category = st.text_input("Dispute category", value="routine", key="routing_test_category")
        risk_level = st.selectbox(
            "Risk level",
            ["low", "medium", "high"],
            index=0,
            key="routing_test_risk"
        )
        submitted = st.form_submit_button("Run routing test")

    if submitted:
        if not rules:
            st.warning("No routing rules are loaded. Upload YAML rules first.")
            return

        transaction = {
            "amount": float(amount),
            "country": country.strip(),
            "category": category.strip(),
            "risk_level": risk_level,
        }

        matches = match_routing_rules(rules, transaction)
        if not matches:
            st.info("No routing rule matched this transaction.")
            return

        selected_rule = matches[0]
        st.success(
            f"Matched rule: **{selected_rule['name']}** → {selected_rule['destination']} "
            f"(Priority: {selected_rule.get('priority', 'n/a')})"
        )
        if len(matches) > 1:
            st.markdown("**Other matching rules:**")
            extra_table = build_routing_table(matches[1:])
            st.dataframe(extra_table, use_container_width=True, hide_index=True)


def render():
    st.header("🧭 Routing Rules")
    st.markdown(
        "Create, validate, and test routing logic using YAML rules for dispute routing and escalation workflows."
    )

    st.markdown("---")
    rules = render_yaml_upload_section()

    st.markdown("---")
    render_routing_rule_table(rules)

    st.markdown("---")
    render_test_routing_form(rules)

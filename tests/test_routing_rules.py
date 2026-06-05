import pytest
from app.components.rule_table import build_rule_dataframe, get_rule_counts, normalize_rule_status
from app.utils.helpers import (
    build_routing_table,
    evaluate_routing_rule,
    match_routing_rules,
    parse_routing_yaml,
    validate_routing_rules,
)


SAMPLE_YAML = """rules:
  - name: High value review
    condition: amount > 1000 and category == \"premium\"
    priority: high
    destination: Senior Review Team
    status: active

  - name: Low value auto-approve
    condition: amount <= 100 and category == \"routine\"
    priority: low
    destination: Auto-approve Queue
    status: active
"""


def test_parse_routing_yaml_returns_rules():
    rules, errors = parse_routing_yaml(SAMPLE_YAML)
    assert not errors
    assert isinstance(rules, list)
    assert len(rules) == 2
    assert rules[0]["name"] == "High value review"
    assert rules[1]["destination"] == "Auto-approve Queue"


def test_validate_routing_rules_detects_missing_fields():
    invalid_yaml = "rules:\n  - name: \"No destination rule\"\n    priority: medium\n"
    rules, parse_errors = parse_routing_yaml(invalid_yaml)
    assert not parse_errors

    messages = validate_routing_rules(rules)
    assert any(msg["severity"] == "error" and "missing a destination" in msg["text"].lower() for msg in messages)


def test_evaluate_routing_rule_matches_expression():
    rule = {
        "name": "High value review",
        "condition": "amount > 1000 and category == \"premium\"",
        "priority": "high",
        "destination": "Senior Review Team",
    }
    transaction = {"amount": 1500.0, "country": "US", "category": "premium", "risk_level": "medium"}
    assert evaluate_routing_rule(rule, transaction) is True

    transaction["amount"] = 500.0
    assert evaluate_routing_rule(rule, transaction) is False


def test_match_routing_rules_returns_highest_priority_match():
    rules = [
        {"name": "Simple low", "condition": "amount < 100", "priority": "low", "destination": "Queue A", "status": "active"},
        {"name": "High priority", "condition": "amount < 100", "priority": "high", "destination": "Queue B", "status": "active"},
    ]
    transaction = {"amount": 50.0, "country": "US", "category": "routine", "risk_level": "low"}
    matches = match_routing_rules(rules, transaction)
    assert len(matches) == 2
    assert matches[0]["destination"] == "Queue B"


def test_build_routing_table_constructs_dataframe():
    rules = [
        {"name": "Test", "condition": "amount > 0", "priority": "medium", "destination": "Queue X", "status": "active"}
    ]
    table = build_routing_table(rules)
    assert table.loc[0, "Name"] == "Test"
    assert table.loc[0, "Destination"] == "Queue X"


def test_get_rule_counts_identifies_active_and_inactive():
    rules = [
        {"name": "Active rule", "status": "active"},
        {"name": "Inactive rule", "status": "inactive"},
    ]
    counts = get_rule_counts(rules)
    assert counts["total"] == 2
    assert counts["active"] == 1
    assert counts["inactive"] == 1


def test_build_rule_dataframe_includes_status_normalization():
    rules = [
        {"name": "Rule", "condition": "amount > 0", "priority": "high", "destination": "Queue", "status": "ACTIVE"}
    ]
    table = build_rule_dataframe(rules)
    assert table.loc[0, "Status"] == "active"
    assert table.loc[0, "Priority"] == "high"
    assert table.loc[0, "Condition"] == "amount > 0"

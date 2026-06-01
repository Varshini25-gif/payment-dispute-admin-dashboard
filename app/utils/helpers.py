"""
Utility Helper Functions
Common helper functions used throughout the application
"""

import ast
import streamlit as st
import pandas as pd
from datetime import datetime
import re


def format_currency(amount):
    """Format amount as currency"""
    if isinstance(amount, (int, float)):
        return f"${amount:,.2f}"
    return amount


def format_date(date_obj):
    """Format date object to readable string"""
    if isinstance(date_obj, datetime):
        return date_obj.strftime("%Y-%m-%d %H:%M:%S")
    return str(date_obj)


def format_status(status):
    """Format status with styling"""
    status_colors = {
        "pending": "🟡",
        "in_review": "🔵",
        "resolved": "🟢",
        "rejected": "🔴",
        "active": "🟢",
        "inactive": "🔴"
    }
    
    status_lower = status.lower().replace(" ", "_")
    icon = status_colors.get(status_lower, "⚪")
    return f"{icon} {status}"


def format_priority(priority):
    """Format priority with styling"""
    priority_colors = {
        "low": "🟢",
        "medium": "🟡",
        "high": "🔴"
    }
    
    priority_lower = priority.lower()
    icon = priority_colors.get(priority_lower, "⚪")
    return f"{icon} {priority}"


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone):
    """Validate phone number format"""
    pattern = r'^[\d\s\-\+\(\)]{10,}$'
    return re.match(pattern, phone) is not None


def truncate_text(text, max_length=50):
    """Truncate text to maximum length"""
    if len(text) > max_length:
        return text[:max_length-3] + "..."
    return text


def get_status_badge_color(status):
    """Get badge color based on status"""
    status_lower = status.lower()
    if status_lower in ["pending", "in_review"]:
        return "yellow"
    elif status_lower in ["resolved", "completed", "active"]:
        return "green"
    elif status_lower in ["rejected", "failed", "inactive"]:
        return "red"
    return "gray"


def get_priority_badge_color(priority):
    """Get badge color based on priority"""
    priority_lower = priority.lower()
    if priority_lower == "high":
        return "red"
    elif priority_lower == "medium":
        return "yellow"
    elif priority_lower == "low":
        return "green"
    return "gray"


def show_success_message(message):
    """Show success notification"""
    st.success(f"✅ {message}")


def show_error_message(message):
    """Show error notification"""
    st.error(f"❌ {message}")


def show_info_message(message):
    """Show info notification"""
    st.info(f"ℹ️ {message}")


def show_warning_message(message):
    """Show warning notification"""
    st.warning(f"⚠️ {message}")


def get_page_title_with_icon(icon, title):
    """Create page title with icon"""
    return f"{icon} {title}"


def parse_routing_yaml(yaml_text):
    """Parse a simple YAML-like routing rule definition."""
    if not isinstance(yaml_text, str):
        return [], ["Routing YAML input must be text."]

    rules = []
    current_rule = None
    parse_errors = []

    for raw_line in yaml_text.splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue

        stripped = line.lstrip()
        if stripped.startswith("- "):
            if current_rule:
                rules.append(current_rule)
            current_rule = {}
            entry = stripped[2:]
            if ":" in entry:
                key, value = entry.split(":", 1)
                current_rule[key.strip()] = value.strip().strip('"').strip("'")
        elif ":" in stripped and current_rule is not None:
            key, value = stripped.split(":", 1)
            current_rule[key.strip()] = value.strip().strip('"').strip("'")
        elif stripped == "rules:" or stripped == "-":
            continue
        else:
            parse_errors.append(f"Unable to parse line: {line}")

    if current_rule:
        rules.append(current_rule)

    return rules, parse_errors


def _evaluate_condition_expression(expression, variables):
    class _SafeEvaluator(ast.NodeVisitor):
        def visit(self, node):
            if isinstance(node, ast.Expr):
                return self.visit(node.value)
            return super().visit(node)

        def visit_Expression(self, node):
            return self.visit(node.body)

        def visit_Constant(self, node):
            return node.value

        def visit_Name(self, node):
            if node.id not in variables:
                raise ValueError(f"Unknown field in condition: {node.id}")
            return variables[node.id]

        def visit_BoolOp(self, node):
            values = [self.visit(value) for value in node.values]
            if isinstance(node.op, ast.And):
                return all(values)
            if isinstance(node.op, ast.Or):
                return any(values)
            raise ValueError("Unsupported boolean operator")

        def visit_Compare(self, node):
            left = self.visit(node.left)
            comparisons = []
            for op, comparator in zip(node.ops, node.comparators):
                right = self.visit(comparator)
                if isinstance(op, ast.Eq):
                    comparisons.append(left == right)
                elif isinstance(op, ast.NotEq):
                    comparisons.append(left != right)
                elif isinstance(op, ast.Gt):
                    comparisons.append(left > right)
                elif isinstance(op, ast.Lt):
                    comparisons.append(left < right)
                elif isinstance(op, ast.GtE):
                    comparisons.append(left >= right)
                elif isinstance(op, ast.LtE):
                    comparisons.append(left <= right)
                elif isinstance(op, ast.In):
                    comparisons.append(left in right)
                elif isinstance(op, ast.NotIn):
                    comparisons.append(left not in right)
                else:
                    raise ValueError("Unsupported comparison operator")
                left = right
            return all(comparisons)

        def visit_BinOp(self, node):
            left = self.visit(node.left)
            right = self.visit(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                return left / right
            raise ValueError("Unsupported arithmetic operator")

        def visit_UnaryOp(self, node):
            operand = self.visit(node.operand)
            if isinstance(node.op, ast.Not):
                return not operand
            if isinstance(node.op, ast.USub):
                return -operand
            raise ValueError("Unsupported unary operator")

        def visit_List(self, node):
            return [self.visit(element) for element in node.elts]

        def visit_Tuple(self, node):
            return tuple(self.visit(element) for element in node.elts)

        def generic_visit(self, node):
            node_type = type(node).__name__
            raise ValueError(f"Unsupported expression element: {node_type}")

    parsed = ast.parse(expression, mode="eval")
    return _SafeEvaluator().visit(parsed)


def evaluate_routing_rule(rule, transaction):
    condition = str(rule.get("condition", "")).strip()
    if not condition:
        return True

    variables = {
        "amount": float(transaction.get("amount", 0.0)),
        "country": str(transaction.get("country", "")),
        "category": str(transaction.get("category", "")),
        "risk_level": str(transaction.get("risk_level", "")),
    }

    try:
        return bool(_evaluate_condition_expression(condition, variables))
    except Exception:
        return False


def match_routing_rules(rules, transaction):
    matches = []
    for rule in rules:
        status = str(rule.get("status", "active")).strip().lower()
        if status == "inactive":
            continue
        if evaluate_routing_rule(rule, transaction):
            matches.append(rule)

    priority_rank = {"high": 3, "medium": 2, "low": 1}
    return sorted(
        matches,
        key=lambda item: priority_rank.get(str(item.get("priority", "")).lower(), 0),
        reverse=True,
    )


def validate_routing_rules(rules):
    messages = []
    if not isinstance(rules, list):
        return [{"severity": "error", "text": "Routing rules must be a list."}]

    if not rules:
        messages.append({"severity": "warning", "text": "No rules were parsed from the YAML content."})
        return messages

    for index, rule in enumerate(rules, start=1):
        name = rule.get("name", "").strip()
        destination = rule.get("destination", "").strip()
        priority = rule.get("priority", "").strip().lower()
        condition = rule.get("condition", "").strip()

        if not name:
            messages.append({"severity": "error", "text": f"Rule {index} is missing a name."})
        if not destination:
            messages.append({"severity": "error", "text": f"Rule {index} is missing a destination."})
        if priority not in ["low", "medium", "high"]:
            messages.append({"severity": "warning", "text": f"Rule {index} uses an unexpected priority '{rule.get('priority', '')}'. Use low, medium, or high."})

        if condition:
            try:
                _evaluate_condition_expression(condition, {
                    "amount": 1.0,
                    "country": "US",
                    "category": "sample",
                    "risk_level": "low",
                })
            except ValueError as exc:
                messages.append({"severity": "error", "text": f"Rule {index} condition error: {exc}"})

    return messages


def build_routing_table(rules):
    rows = []
    for rule in rules:
        rows.append({
            "Name": rule.get("name", ""),
            "Condition": rule.get("condition", ""),
            "Priority": rule.get("priority", ""),
            "Destination": rule.get("destination", ""),
            "Status": rule.get("status", "active"),
        })
    return pd.DataFrame(rows)

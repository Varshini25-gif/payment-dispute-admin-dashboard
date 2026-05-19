"""
Utility Helper Functions
Common helper functions used throughout the application
"""

import streamlit as st
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

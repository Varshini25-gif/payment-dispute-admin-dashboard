"""
Unit tests for utility helpers
"""

import pytest
from app.utils.helpers import (
    format_currency,
    format_date,
    format_status,
    format_priority,
    validate_email,
    validate_phone,
    truncate_text
)
from datetime import datetime


class TestFormatters:
    """Test formatter functions"""
    
    def test_format_currency(self):
        assert format_currency(100) == "$100.00"
        assert format_currency(1234.56) == "$1,234.56"
        assert format_currency("text") == "text"
    
    def test_format_date(self):
        date_obj = datetime(2024, 5, 19, 10, 30, 0)
        result = format_date(date_obj)
        assert result == "2024-05-19 10:30:00"
    
    def test_format_status(self):
        assert "🟡" in format_status("pending")
        assert "🟢" in format_status("resolved")
        assert "🔴" in format_status("rejected")
    
    def test_format_priority(self):
        assert "🟢" in format_priority("low")
        assert "🟡" in format_priority("medium")
        assert "🔴" in format_priority("high")


class TestValidators:
    """Test validator functions"""
    
    def test_validate_email_valid(self):
        assert validate_email("user@example.com") is True
        assert validate_email("admin@company.co.uk") is True
    
    def test_validate_email_invalid(self):
        assert validate_email("invalid_email") is False
        assert validate_email("@example.com") is False
    
    def test_validate_phone_valid(self):
        assert validate_phone("1234567890") is True
        assert validate_phone("+1-234-567-8900") is True
    
    def test_validate_phone_invalid(self):
        assert validate_phone("123") is False
        assert validate_phone("abc") is False
    
    def test_truncate_text(self):
        text = "This is a long text that should be truncated"
        result = truncate_text(text, max_length=20)
        assert len(result) <= 20
        assert result.endswith("...")
        
        short_text = "Short"
        assert truncate_text(short_text) == "Short"

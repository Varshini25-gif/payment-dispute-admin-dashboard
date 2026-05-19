"""
Validation Utilities
Functions for validating and sanitizing user input
"""

import re
from datetime import datetime


class ValidationError(Exception):
    """Custom validation error"""
    pass


class Validator:
    """Main validator class"""
    
    @staticmethod
    def validate_string(value, min_length=None, max_length=None, required=True):
        """Validate string input"""
        if required and (value is None or value == ""):
            raise ValidationError("This field is required")
        
        if value is None or value == "":
            return True
        
        if not isinstance(value, str):
            raise ValidationError("Must be a string")
        
        if min_length and len(value) < min_length:
            raise ValidationError(f"Minimum length is {min_length}")
        
        if max_length and len(value) > max_length:
            raise ValidationError(f"Maximum length is {max_length}")
        
        return True
    
    @staticmethod
    def validate_email(email):
        """Validate email address"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValidationError("Invalid email address")
        return True
    
    @staticmethod
    def validate_phone(phone):
        """Validate phone number"""
        pattern = r'^[\d\s\-\+\(\)]{10,}$'
        if not re.match(pattern, phone):
            raise ValidationError("Invalid phone number format")
        return True
    
    @staticmethod
    def validate_number(value, min_value=None, max_value=None):
        """Validate numeric input"""
        if not isinstance(value, (int, float)):
            raise ValidationError("Must be a number")
        
        if min_value is not None and value < min_value:
            raise ValidationError(f"Minimum value is {min_value}")
        
        if max_value is not None and value > max_value:
            raise ValidationError(f"Maximum value is {max_value}")
        
        return True
    
    @staticmethod
    def validate_date(date_str, date_format="%Y-%m-%d"):
        """Validate date format"""
        try:
            datetime.strptime(date_str, date_format)
            return True
        except ValueError:
            raise ValidationError(f"Invalid date format. Use {date_format}")
    
    @staticmethod
    def validate_choice(value, choices):
        """Validate value is in allowed choices"""
        if value not in choices:
            raise ValidationError(f"Must be one of: {', '.join(choices)}")
        return True
    
    @staticmethod
    def validate_currency(value):
        """Validate currency amount"""
        try:
            amount = float(value)
            if amount < 0:
                raise ValidationError("Amount cannot be negative")
            return True
        except ValueError:
            raise ValidationError("Invalid currency amount")
    
    @staticmethod
    def validate_url(url):
        """Validate URL format"""
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        if not re.match(pattern, url):
            raise ValidationError("Invalid URL format")
        return True
    
    @staticmethod
    def sanitize_string(value):
        """Sanitize string input"""
        if not isinstance(value, str):
            return value
        return value.strip()
    
    @staticmethod
    def sanitize_html(value):
        """Remove potentially dangerous HTML tags"""
        if not isinstance(value, str):
            return value
        
        # Remove script tags and content
        value = re.sub(r'<script[^>]*>.*?</script>', '', value, flags=re.DOTALL)
        # Remove event attributes
        value = re.sub(r'\s?on\w+\s*=\s*["\'].*?["\']', '', value)
        
        return value


def validate_dispute_data(dispute_data):
    """Validate complete dispute data"""
    validator = Validator()
    
    # Validate required fields
    if "amount" not in dispute_data or dispute_data["amount"] is None:
        raise ValidationError("Amount is required")
    
    if "status" not in dispute_data:
        raise ValidationError("Status is required")
    
    # Validate amount
    validator.validate_currency(dispute_data["amount"])
    
    # Validate status
    valid_statuses = ["pending", "in_review", "resolved", "rejected"]
    validator.validate_choice(dispute_data["status"], valid_statuses)
    
    # Validate priority if present
    if "priority" in dispute_data and dispute_data["priority"]:
        valid_priorities = ["low", "medium", "high"]
        validator.validate_choice(dispute_data["priority"], valid_priorities)
    
    return True


def validate_user_data(user_data):
    """Validate complete user data"""
    validator = Validator()
    
    # Validate required fields
    if "username" not in user_data or not user_data["username"]:
        raise ValidationError("Username is required")
    
    if "email" not in user_data or not user_data["email"]:
        raise ValidationError("Email is required")
    
    # Validate username
    validator.validate_string(user_data["username"], min_length=3, max_length=50)
    
    # Validate email
    validator.validate_email(user_data["email"])
    
    # Validate password if present
    if "password" in user_data and user_data["password"]:
        validator.validate_string(user_data["password"], min_length=8)
    
    return True

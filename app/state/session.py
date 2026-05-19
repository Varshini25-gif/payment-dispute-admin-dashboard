"""
Application State Management
Handles session state for the application
"""

import streamlit as st
from datetime import datetime


class SessionState:
    """Application session state manager"""
    
    # User related
    CURRENT_USER = "current_user"
    USER_ROLE = "user_role"
    IS_AUTHENTICATED = "is_authenticated"
    
    # UI related
    SIDEBAR_EXPANDED = "sidebar_expanded"
    CURRENT_PAGE = "current_page"
    THEME_MODE = "theme_mode"
    
    # Data related
    DISPUTES_DATA = "disputes_data"
    USERS_DATA = "users_data"
    LAST_REFRESH = "last_refresh"
    
    # Filter related
    DISPUTE_FILTER = "dispute_filter"
    USER_FILTER = "user_filter"
    
    @staticmethod
    def initialize():
        """Initialize default session state"""
        if SessionState.CURRENT_USER not in st.session_state:
            st.session_state[SessionState.CURRENT_USER] = None
        
        if SessionState.IS_AUTHENTICATED not in st.session_state:
            st.session_state[SessionState.IS_AUTHENTICATED] = False
        
        if SessionState.USER_ROLE not in st.session_state:
            st.session_state[SessionState.USER_ROLE] = "viewer"
        
        if SessionState.SIDEBAR_EXPANDED not in st.session_state:
            st.session_state[SessionState.SIDEBAR_EXPANDED] = True
        
        if SessionState.CURRENT_PAGE not in st.session_state:
            st.session_state[SessionState.CURRENT_PAGE] = "Dashboard"
        
        if SessionState.THEME_MODE not in st.session_state:
            st.session_state[SessionState.THEME_MODE] = "light"
        
        if SessionState.DISPUTES_DATA not in st.session_state:
            st.session_state[SessionState.DISPUTES_DATA] = None
        
        if SessionState.USERS_DATA not in st.session_state:
            st.session_state[SessionState.USERS_DATA] = None
        
        if SessionState.LAST_REFRESH not in st.session_state:
            st.session_state[SessionState.LAST_REFRESH] = None
        
        if SessionState.DISPUTE_FILTER not in st.session_state:
            st.session_state[SessionState.DISPUTE_FILTER] = {}
        
        if SessionState.USER_FILTER not in st.session_state:
            st.session_state[SessionState.USER_FILTER] = {}
    
    @staticmethod
    def set_user(user_data):
        """Set current user"""
        st.session_state[SessionState.CURRENT_USER] = user_data
    
    @staticmethod
    def get_user():
        """Get current user"""
        return st.session_state.get(SessionState.CURRENT_USER)
    
    @staticmethod
    def set_authenticated(value):
        """Set authentication status"""
        st.session_state[SessionState.IS_AUTHENTICATED] = value
    
    @staticmethod
    def is_authenticated():
        """Check if user is authenticated"""
        return st.session_state.get(SessionState.IS_AUTHENTICATED, False)
    
    @staticmethod
    def set_role(role):
        """Set user role"""
        st.session_state[SessionState.USER_ROLE] = role
    
    @staticmethod
    def get_role():
        """Get user role"""
        return st.session_state.get(SessionState.USER_ROLE, "viewer")
    
    @staticmethod
    def set_page(page_name):
        """Set current page"""
        st.session_state[SessionState.CURRENT_PAGE] = page_name
    
    @staticmethod
    def get_page():
        """Get current page"""
        return st.session_state.get(SessionState.CURRENT_PAGE, "Dashboard")
    
    @staticmethod
    def set_theme(theme):
        """Set theme mode"""
        st.session_state[SessionState.THEME_MODE] = theme
    
    @staticmethod
    def get_theme():
        """Get theme mode"""
        return st.session_state.get(SessionState.THEME_MODE, "light")
    
    @staticmethod
    def set_disputes_data(data):
        """Set disputes data"""
        st.session_state[SessionState.DISPUTES_DATA] = data
        st.session_state[SessionState.LAST_REFRESH] = datetime.now()
    
    @staticmethod
    def get_disputes_data():
        """Get disputes data"""
        return st.session_state.get(SessionState.DISPUTES_DATA)
    
    @staticmethod
    def set_users_data(data):
        """Set users data"""
        st.session_state[SessionState.USERS_DATA] = data
    
    @staticmethod
    def get_users_data():
        """Get users data"""
        return st.session_state.get(SessionState.USERS_DATA)
    
    @staticmethod
    def set_dispute_filter(filter_dict):
        """Set dispute filter"""
        st.session_state[SessionState.DISPUTE_FILTER] = filter_dict
    
    @staticmethod
    def get_dispute_filter():
        """Get dispute filter"""
        return st.session_state.get(SessionState.DISPUTE_FILTER, {})
    
    @staticmethod
    def set_user_filter(filter_dict):
        """Set user filter"""
        st.session_state[SessionState.USER_FILTER] = filter_dict
    
    @staticmethod
    def get_user_filter():
        """Get user filter"""
        return st.session_state.get(SessionState.USER_FILTER, {})
    
    @staticmethod
    def clear_session():
        """Clear all session state"""
        for key in list(st.session_state.keys()):
            del st.session_state[key]


def get_last_refresh_time():
    """Get last refresh time formatted"""
    last_refresh = st.session_state.get(SessionState.LAST_REFRESH)
    if last_refresh:
        return last_refresh.strftime("%Y-%m-%d %H:%M:%S")
    return "Never"

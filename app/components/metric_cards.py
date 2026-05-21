import streamlit as st


def get_dashboard_metrics():
    """Return a list of metric definitions for the dashboard."""
    return [
        {"label": "Total Disputes", "value": "1,234", "delta": "+12 this week", "icon": "📁"},
        {"label": "Pending Disputes", "value": "456", "delta": "-8 this week", "icon": "⏳"},
        {"label": "Resolved Disputes", "value": "678", "delta": "+20 this week", "icon": "✅"},
        {"label": "Resolution Rate", "value": "86.5%", "delta": "+2.3%", "icon": "📈"}
    ]


def render_metric_cards(metrics):
    """Render reusable metric cards in a responsive row."""
    cols = st.columns(len(metrics))
    for metric, col in zip(metrics, cols):
        with col:
            st.markdown("<div style='background: #f8fafc; padding: 16px; border-radius: 12px;'>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 24px; margin-bottom: 8px;'>{metric['icon']}</div>", unsafe_allow_html=True)
            st.metric(label=metric["label"], value=metric["value"], delta=metric.get("delta", ""))
            st.markdown("</div>", unsafe_allow_html=True)

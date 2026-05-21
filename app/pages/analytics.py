import streamlit as st
from app.components.common import render_info_box


def render():
    st.header("📊 Analytics")
    st.markdown("View dispute trends, volume analysis, and team performance metrics.")
    render_info_box(
        "Analytics Coming Soon",
        "The analytics page will include charts, trend forecasts, and KPI tracking dashboards."
    )
    st.markdown("---")
    st.subheader("Highlights")
    st.write("Placeholder for analytics cards and drill-down charts.")

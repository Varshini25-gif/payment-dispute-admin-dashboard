import streamlit as st
import pandas as pd
import plotly.express as px

from app.components.reusable_widgets import (
    render_chart_container_start,
    render_chart_container_end,
    render_empty_state,
)


def _render_plotly_chart(fig):
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#334155"),
        height=250,
    )
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False, "responsive": True},
    )


def render_status_chart():
    """Render a bar chart for dispute status distribution."""
    status_data = pd.DataFrame({
        "Status": ["Pending", "In Review", "Resolved"],
        "Count": [456, 234, 678]
    })
    render_chart_container_start("Disputes by Status", "Current workload split by processing stage.")
    if status_data.empty:
        render_empty_state("No data available", "Status metrics will appear once cases are ingested.")
        render_chart_container_end()
        return

    fig = px.bar(
        status_data,
        x="Status",
        y="Count",
        color="Status",
        color_discrete_sequence=["#f59e0b", "#0ea5e9", "#10b981"],
    )
    _render_plotly_chart(fig)
    render_chart_container_end()


def render_priority_chart():
    """Render a bar chart for dispute priority distribution."""
    priority_data = pd.DataFrame({
        "Priority": ["Low", "Medium", "High"],
        "Count": [300, 450, 618]
    })
    render_chart_container_start("Disputes by Priority", "Prioritization trend across open and active cases.")
    if priority_data.empty:
        render_empty_state("No priority data", "Priority chart is waiting for queue updates.")
        render_chart_container_end()
        return

    fig = px.bar(
        priority_data,
        x="Priority",
        y="Count",
        color="Priority",
        color_discrete_sequence=["#22c55e", "#f59e0b", "#ef4444"],
    )
    _render_plotly_chart(fig)
    render_chart_container_end()


def render_volume_chart():
    """Render an area chart showing monthly dispute volume."""
    volume_data = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Volume": [320, 410, 360, 450, 520, 480]
    })
    render_chart_container_start("Monthly Dispute Volume", "6-month dispute intake trend.")
    if volume_data.empty:
        render_empty_state("No volume data", "Volume chart will populate when historical data is available.")
        render_chart_container_end()
        return

    fig = px.area(
        volume_data,
        x="Month",
        y="Volume",
        markers=True,
        color_discrete_sequence=["#0f766e"],
    )
    _render_plotly_chart(fig)
    render_chart_container_end()

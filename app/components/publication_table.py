"""Confluence publication history table rendering."""

from __future__ import annotations

import pandas as pd
import streamlit as st


def build_publication_table_frame(data: pd.DataFrame) -> pd.DataFrame:
    """Return the display frame used by the publication table."""
    if data is None or data.empty:
        return pd.DataFrame(
            columns=[
                "Publication ID",
                "Page Title",
                "Space Key",
                "Page Link",
                "Publish Status",
                "Published By",
                "Published At",
                "Error Message",
            ]
        )

    frame = data.copy()

    if "Published At" in frame.columns and pd.api.types.is_datetime64_any_dtype(frame["Published At"]):
        frame["Published At"] = frame["Published At"].dt.strftime("%Y-%m-%d %H:%M:%S")

    wanted_columns = [
        "Publication ID",
        "Page Title",
        "Space Key",
        "Page Link",
        "Publish Status",
        "Published By",
        "Published At",
        "Error Message",
    ]
    existing = [column for column in wanted_columns if column in frame.columns]
    return frame[existing]


def render_publication_table(data: pd.DataFrame) -> None:
    """Render publication history table with link and status formatting."""
    frame = build_publication_table_frame(data)
    if frame.empty:
        st.info("No publication records match the current filters.")
        return

    st.dataframe(
        frame,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Page Link": st.column_config.LinkColumn(
                "Page Reference",
                display_text="Open page",
                help="Opens the published Confluence page.",
            ),
            "Error Message": st.column_config.TextColumn(
                "Error",
                width="large",
                help="Failure details when publication does not complete successfully.",
            ),
            "Publish Status": st.column_config.TextColumn(
                "Status",
                width="small",
            ),
        },
    )

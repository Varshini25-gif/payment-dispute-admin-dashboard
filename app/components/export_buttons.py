"""Export button helpers for dataframe downloads."""

from __future__ import annotations

from datetime import datetime

import pandas as pd
import streamlit as st


def dataframe_to_csv_bytes(dataframe: pd.DataFrame) -> bytes:
    """Convert a dataframe into UTF-8 CSV bytes."""
    if dataframe is None or dataframe.empty:
        return b""
    return dataframe.to_csv(index=False).encode("utf-8")


def render_csv_export_button(
    dataframe: pd.DataFrame,
    file_prefix: str = "disputes",
    label: str = "⬇️ Export CSV",
    key: str = "disputes_export_csv",
) -> None:
    """Render a Streamlit CSV export button for the provided dataframe."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.download_button(
        label=label,
        data=dataframe_to_csv_bytes(dataframe),
        file_name=f"{file_prefix}_{timestamp}.csv",
        mime="text/csv",
        disabled=dataframe is None or dataframe.empty,
        key=key,
        use_container_width=True,
    )

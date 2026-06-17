"""
Activity timeline component
Renders a vertical chronological timeline of recent audit events.
"""

from datetime import datetime
import streamlit as st


# Status → (emoji, CSS colour)
_STATUS_STYLE: dict[str, tuple[str, str]] = {
    "Success": ("✅", "#22c55e"),
    "Failure": ("❌", "#ef4444"),
    "Warning": ("⚠️", "#f59e0b"),
    "Info":    ("ℹ️", "#3b82f6"),
}

# Action keyword → icon
_ACTION_ICONS: dict[str, str] = {
    "Created": "🆕",
    "Updated": "✏️",
    "Resolved": "✔️",
    "Closed": "🔒",
    "Escalated": "🔺",
    "Assigned": "👤",
    "Uploaded": "📎",
    "Submitted": "📬",
    "Issued": "💸",
    "Requested": "📋",
    "Changed": "🔄",
    "Added": "💬",
    "Login": "🔐",
    "Logout": "🚪",
    "Generated": "📤",
}


def _action_icon(action: str) -> str:
    for keyword, icon in _ACTION_ICONS.items():
        if keyword.lower() in action.lower():
            return icon
    return "📌"


def render_activity_timeline(events: list[dict], title: str = "Recent Activity") -> None:
    """
    Render a vertical timeline of audit events.

    Parameters
    ----------
    events : list[dict]
        Each dict must contain at minimum:
          - ``Timestamp`` – str or datetime
          - ``Action``    – str
          - ``Actor``     – str
          - ``Dispute ID``– str
          - ``Status``    – str
          - ``Details``   – str  (optional)
    title : str
        Section heading shown above the timeline.
    """
    st.subheader(f"🕐 {title}")

    if not events:
        st.info("No recent activity to display.")
        return

    # CSS injected once
    st.markdown(
        """
        <style>
        .tl-container { position: relative; padding-left: 28px; }
        .tl-line {
            position: absolute; left: 11px; top: 0; bottom: 0;
            width: 2px; background: #e2e8f0;
        }
        .tl-item { position: relative; margin-bottom: 18px; }
        .tl-dot {
            position: absolute; left: -22px; top: 4px;
            width: 14px; height: 14px; border-radius: 50%;
            border: 2px solid #fff; box-shadow: 0 0 0 2px #cbd5e1;
        }
        .tl-card {
            background: #f8fafc; border: 1px solid #e2e8f0;
            border-radius: 8px; padding: 10px 14px;
        }
        .tl-header { display: flex; align-items: center; gap: 8px;
                     flex-wrap: wrap; margin-bottom: 4px; }
        .tl-action { font-weight: 600; font-size: 0.92rem; }
        .tl-badge {
            font-size: 0.72rem; padding: 2px 8px;
            border-radius: 12px; font-weight: 600;
        }
        .tl-meta { font-size: 0.78rem; color: #64748b; }
        .tl-details { font-size: 0.82rem; color: #475569; margin-top: 4px; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    items_html = ""
    for event in events:
        ts = event.get("Timestamp", "")
        if isinstance(ts, datetime):
            ts_str = ts.strftime("%Y-%m-%d %H:%M")
        else:
            ts_str = str(ts)[:16] if ts else "—"

        action = event.get("Action", "Unknown")
        actor = event.get("Actor", "—")
        dispute = event.get("Dispute ID", "—")
        status = event.get("Status", "Info")
        details = event.get("Details", "")

        icon = _action_icon(action)
        s_icon, s_color = _STATUS_STYLE.get(status, ("•", "#94a3b8"))

        items_html += f"""
        <div class="tl-item">
          <div class="tl-dot" style="background:{s_color};"></div>
          <div class="tl-card">
            <div class="tl-header">
              <span class="tl-action">{icon} {action}</span>
              <span class="tl-badge" style="background:{s_color}22;color:{s_color};">
                {s_icon} {status}
              </span>
              <span class="tl-badge" style="background:#f1f5f9;color:#334155;">
                {dispute}
              </span>
            </div>
            <div class="tl-meta">🕐 {ts_str} &nbsp;|&nbsp; 👤 {actor}</div>
            {f'<div class="tl-details">{details}</div>' if details else ''}
          </div>
        </div>
        """

    st.markdown(
        f'<div class="tl-container"><div class="tl-line"></div>{items_html}</div>',
        unsafe_allow_html=True,
    )


def render_activity_summary_badges(summary: dict) -> None:
    """
    Render small coloured badge metrics for the timeline section.

    Parameters
    ----------
    summary : dict  keys: total, success, warning, failure, info
    """
    badges = [
        ("Total Events",  summary.get("total", 0),   "#6366f1"),
        ("✅ Success",     summary.get("success", 0), "#22c55e"),
        ("⚠️ Warning",    summary.get("warning", 0), "#f59e0b"),
        ("❌ Failure",    summary.get("failure", 0), "#ef4444"),
        ("ℹ️ Info",       summary.get("info", 0),    "#3b82f6"),
    ]
    cols = st.columns(len(badges))
    for col, (label, value, color) in zip(cols, badges):
        col.markdown(
            f"""
            <div style="background:{color}15;border:1px solid {color}40;
                        border-radius:8px;padding:10px;text-align:center;">
              <div style="font-size:1.4rem;font-weight:700;color:{color};">{value}</div>
              <div style="font-size:0.78rem;color:#64748b;">{label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

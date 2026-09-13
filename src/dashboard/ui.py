from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image

from src.config import ROOT_DIR, Settings, get_settings
from src.services.dashboard_service import DashboardService


def inject_css() -> None:
    css_path = ROOT_DIR / "assets" / "styles" / "dashboard.css"
    st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def render_shell(title: str, subtitle: str, role: str) -> None:
    st.markdown(
        f"""
        <div class="hero-shell">
            <div class="status-pill">Role: {role.upper()}</div>
            <div class="hero-title">{title}</div>
            <div class="hero-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_cards(metrics: dict) -> None:
    columns = st.columns(4)
    items = [
        ("Registered Staff", metrics["registered_people"], "Total enrolled employees"),
        ("Present Today", metrics["today_present"], "Unique people marked today"),
        ("Monthly Records", metrics["month_present"], "Attendance rows for this month"),
        ("Unknown Faces", metrics["unknown_faces"], "Unrecognized detections today"),
    ]
    for column, (label, value, note) in zip(columns, items):
        with column:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-footnote">{note}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _safe_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    return df if not df.empty else pd.DataFrame([{"Info": "No records yet"}])


def render_overview_page(service: DashboardService) -> None:
    metrics = service.metrics()
    render_metric_cards(metrics)
    st.markdown("")

    daily_df = service.daily_attendance_df()
    monthly_df = service.monthly_attendance_df()
    person_df = service.person_wise_df()

    left, right = st.columns((1.4, 1), gap="large")
    with left:
        st.markdown('<div class="section-title">Daily Attendance</div>', unsafe_allow_html=True)
        figure = px.area(
            daily_df,
            x="date",
            y="count",
            markers=True,
            color_discrete_sequence=["#15c39a"],
        )
        figure.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e5eef8",
            margin=dict(l=8, r=8, t=8, b=8),
        )
        st.plotly_chart(figure, use_container_width=True)

    with right:
        st.markdown('<div class="section-title">Monthly Analytics</div>', unsafe_allow_html=True)
        figure = px.bar(
            monthly_df,
            x="month",
            y="count",
            color="count",
            color_continuous_scale=["#10324b", "#4da8ff"],
        )
        figure.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e5eef8",
            margin=dict(l=8, r=8, t=8, b=8),
            coloraxis_showscale=False,
        )
        st.plotly_chart(figure, use_container_width=True)

    st.markdown('<div class="section-title">Person Wise Count</div>', unsafe_allow_html=True)
    figure = px.bar(
        person_df,
        x="attendance_count",
        y="full_name",
        orientation="h",
        text="attendance_count",
        color="attendance_count",
        color_continuous_scale=["#12253a", "#15c39a"],
    )
    figure.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e5eef8",
        margin=dict(l=8, r=8, t=8, b=8),
        coloraxis_showscale=False,
        yaxis_title="",
        xaxis_title="Attendance Count",
    )
    st.plotly_chart(figure, use_container_width=True)


def render_live_monitor_page(service: DashboardService, settings: Settings | None = None) -> None:
    settings = settings or get_settings()
    left, right = st.columns((1.35, 1), gap="large")
    with left:
        st.markdown('<div class="section-title">Live Camera Snapshot</div>', unsafe_allow_html=True)
        if settings.live_frame_full_path.exists():
            image = Image.open(settings.live_frame_full_path)
            st.image(image, use_container_width=True, caption="Last processed frame")
        else:
            st.info("No live frame available yet. Start `python run_camera.py` to generate snapshots.")

    with right:
        st.markdown('<div class="section-title">Recent Recognition Events</div>', unsafe_allow_html=True)
        st.dataframe(_safe_dataframe(service.recent_events_df()), use_container_width=True, hide_index=True)


def render_people_page(service: DashboardService) -> None:
    st.markdown('<div class="section-title">Registered People</div>', unsafe_allow_html=True)
    st.dataframe(_safe_dataframe(service.people_df()), use_container_width=True, hide_index=True)
    st.markdown(
        """
        <div class="small-muted">
            Add employee folders inside <code>data/known_faces</code> and run <code>python scripts/enroll_faces.py</code>
            to generate FaceNet embeddings and sync employee records.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_alerts_page(service: DashboardService) -> None:
    st.markdown('<div class="section-title">Alert Activity</div>', unsafe_allow_html=True)
    st.dataframe(_safe_dataframe(service.alerts_df()), use_container_width=True, hide_index=True)


def render_system_page(settings: Settings) -> None:
    st.markdown('<div class="section-title">System Runtime</div>', unsafe_allow_html=True)
    runtime_df = pd.DataFrame(
        [
            {"Setting": "Application", "Value": settings.app_name},
            {"Setting": "Theme", "Value": settings.app_theme},
            {"Setting": "Camera Index", "Value": settings.camera_index},
            {"Setting": "Database", "Value": settings.db_name},
            {"Setting": "SQL Server", "Value": settings.db_server},
            {"Setting": "Face Threshold", "Value": settings.face_match_threshold},
            {"Setting": "Duplicate Cooldown (s)", "Value": settings.duplicate_cooldown_seconds},
            {"Setting": "Email Alerts", "Value": settings.smtp_enabled},
            {"Setting": "SMS Alerts", "Value": settings.twilio_enabled},
        ]
    )
    st.dataframe(runtime_df, use_container_width=True, hide_index=True)
    st.code(
        "python scripts/bootstrap_db.py\npython scripts/enroll_faces.py\npython run_camera.py\nstreamlit run app.py",
        language="powershell",
    )


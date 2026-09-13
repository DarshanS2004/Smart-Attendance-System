from __future__ import annotations

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from src.config import get_settings
from src.dashboard.ui import (
    inject_css,
    render_alerts_page,
    render_live_monitor_page,
    render_overview_page,
    render_people_page,
    render_shell,
    render_system_page,
)
from src.database.db import DatabaseManager
from src.database.repository import AttendanceRepository
from src.services.dashboard_service import DashboardService


settings = get_settings()
startup_error = None
repository = None
dashboard_service = None

try:
    database = DatabaseManager(settings)
    database.bootstrap()
    repository = AttendanceRepository(database)
    dashboard_service = DashboardService(repository, settings)
except Exception as exc:
    startup_error = str(exc)


def init_state() -> None:
    st.session_state.setdefault("authenticated", False)
    st.session_state.setdefault("user", None)


def login_view() -> None:
    left, center, right = st.columns((1, 1.35, 1))
    with center:
        st.markdown(
            """
            <div class="hero-shell">
                <div class="hero-title">Smart Attendance System</div>
                <div class="hero-subtitle">
                    Premium real-time attendance intelligence with face recognition, tracking,
                    SQL Server analytics, and alerting.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("")
        with st.form("login-form", clear_on_submit=False):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Secure Login", use_container_width=True)
            if submitted:
                user = repository.authenticate_user(username, password)
                if user:
                    st.session_state["authenticated"] = True
                    st.session_state["user"] = user
                    st.rerun()
                st.error("Invalid username or password.")

        st.caption("Default accounts: admin / hr / viewer")


def app_view() -> None:
    if dashboard_service is None:
        st.error(
            "Database bootstrap failed. Check your SQL Server instance, ODBC driver, and `.env` settings."
        )
        st.code(startup_error or "Unknown startup error", language="text")
        return

    st_autorefresh(interval=4_000, key="dashboard-refresh")
    user = st.session_state["user"]
    with st.sidebar:
        st.markdown("## Command Center")
        page = st.radio(
            "Navigation",
            ["Overview", "Live Monitor", "People", "Alerts", "System"],
            label_visibility="collapsed",
        )
        st.markdown("---")
        st.markdown(f"**User:** {user['username']}")
        st.markdown(f"**Role:** {user['role']}")
        if st.button("Logout", use_container_width=True):
            st.session_state["authenticated"] = False
            st.session_state["user"] = None
            st.rerun()

    render_shell(
        title=settings.app_name,
        subtitle="Real-time face recognition attendance, duplicate control, live monitoring, monthly analytics, and alert automation in one premium dashboard.",
        role=user["role"],
    )
    st.markdown("")

    if page == "Overview":
        render_overview_page(dashboard_service)
    elif page == "Live Monitor":
        render_live_monitor_page(dashboard_service, settings)
    elif page == "People":
        render_people_page(dashboard_service)
    elif page == "Alerts":
        render_alerts_page(dashboard_service)
    else:
        render_system_page(settings)


def main() -> None:
    st.set_page_config(
        page_title=settings.app_name,
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_css()
    init_state()
    if startup_error:
        st.error("Startup failed before authentication. Review the details below.")
        st.code(startup_error, language="text")
        st.info(
            "If SQL Server is running but still unreachable, try starting SQL Browser or update the host/port in `.env`."
        )
        return
    if not st.session_state["authenticated"]:
        login_view()
    else:
        app_view()


if __name__ == "__main__":
    main()

from __future__ import annotations

import pandas as pd

from src.config import Settings, get_settings
from src.database.repository import AttendanceRepository


class DashboardService:
    def __init__(self, repository: AttendanceRepository, settings: Settings | None = None) -> None:
        self.repository = repository
        self.settings = settings or get_settings()

    def metrics(self) -> dict:
        return self.repository.get_overview_metrics()

    def daily_attendance_df(self) -> pd.DataFrame:
        rows = self.repository.get_daily_attendance(days=10)
        return pd.DataFrame(rows or [{"date": pd.Timestamp.now().date(), "count": 0}])

    def monthly_attendance_df(self) -> pd.DataFrame:
        rows = self.repository.get_monthly_attendance(months=6)
        return pd.DataFrame(rows or [{"month": "N/A", "count": 0}])

    def person_wise_df(self) -> pd.DataFrame:
        rows = self.repository.get_person_wise_counts(limit=20)
        return pd.DataFrame(rows or [{"full_name": "No data", "employee_code": "-", "attendance_count": 0}])

    def recent_events_df(self) -> pd.DataFrame:
        rows = self.repository.get_recent_events(limit=25)
        return pd.DataFrame(rows)

    def alerts_df(self) -> pd.DataFrame:
        rows = self.repository.get_alert_logs(limit=25)
        return pd.DataFrame(rows)

    def people_df(self) -> pd.DataFrame:
        rows = self.repository.list_people()
        return pd.DataFrame(rows)


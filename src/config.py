from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.engine import URL


ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")
load_dotenv(ROOT_DIR / ".env.example", override=False)


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _as_int(value: str | None, default: int) -> int:
    if value is None or value == "":
        return default
    return int(value)


def _as_float(value: str | None, default: float) -> float:
    if value is None or value == "":
        return default
    return float(value)


def _as_list(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


@dataclass(frozen=True)
class Settings:
    app_name: str
    app_theme: str
    app_secret_key: str
    timezone: str
    camera_index: int
    camera_width: int
    camera_height: int
    frame_skip: int
    save_live_frame: bool
    live_frame_path: str
    db_server: str
    db_port: int
    db_name: str
    db_driver: str
    db_use_windows_auth: bool
    db_username: str
    db_password: str
    face_match_threshold: float
    duplicate_cooldown_seconds: int
    unknown_alert_cooldown_seconds: int
    yolo_face_model: str
    yolo_fallback_model: str
    embeddings_path: str
    known_faces_dir: str
    smtp_enabled: bool
    smtp_server: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    alert_email_recipients: list[str]
    twilio_enabled: bool
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_from_number: str
    twilio_to_numbers: list[str]
    admin_username: str
    admin_password: str
    hr_username: str
    hr_password: str
    viewer_username: str
    viewer_password: str

    @property
    def live_frame_full_path(self) -> Path:
        return ROOT_DIR / self.live_frame_path

    @property
    def embeddings_full_path(self) -> Path:
        return ROOT_DIR / self.embeddings_path

    @property
    def known_faces_full_path(self) -> Path:
        return ROOT_DIR / self.known_faces_dir

    @property
    def yolo_face_model_full_path(self) -> Path:
        return ROOT_DIR / self.yolo_face_model

    def sqlalchemy_url(self, database: str | None = None) -> URL:
        target_database = database or self.db_name
        query = {
            "driver": self.db_driver,
            "TrustServerCertificate": "yes",
            "Encrypt": "no",
        }
        if self.db_use_windows_auth:
            query["trusted_connection"] = "yes"
            return URL.create(
                "mssql+pyodbc",
                host=self.db_server,
                database=target_database,
                query=query,
            )

        return URL.create(
            "mssql+pyodbc",
            username=self.db_username,
            password=self.db_password,
            host=self.db_server,
            port=self.db_port,
            database=target_database,
            query=query,
        )

    def pyodbc_connection_string(self, database: str) -> str:
        base = (
            f"DRIVER={{{self.db_driver}}};"
            f"SERVER={self.db_server};"
            f"DATABASE={database};"
            "Encrypt=no;"
            "TrustServerCertificate=yes;"
        )
        if self.db_use_windows_auth:
            return base + "Trusted_Connection=yes;"
        return (
            base
            + f"UID={self.db_username};"
            + f"PWD={self.db_password};"
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", "Smart Attendance System"),
        app_theme=os.getenv("APP_THEME", "default premium dark"),
        app_secret_key=os.getenv("APP_SECRET_KEY", "smart-attendance-secret-key"),
        timezone=os.getenv("APP_TIMEZONE", "Asia/Calcutta"),
        camera_index=_as_int(os.getenv("CAMERA_INDEX"), 0),
        camera_width=_as_int(os.getenv("CAMERA_WIDTH"), 1280),
        camera_height=_as_int(os.getenv("CAMERA_HEIGHT"), 720),
        frame_skip=max(_as_int(os.getenv("FRAME_SKIP"), 2), 1),
        save_live_frame=_as_bool(os.getenv("SAVE_LIVE_FRAME"), True),
        live_frame_path=os.getenv("LIVE_FRAME_PATH", "data/exports/live_frame.jpg"),
        db_server=os.getenv("DB_SERVER", r"localhost\SQLEXPRESS"),
        db_port=_as_int(os.getenv("DB_PORT"), 1433),
        db_name=os.getenv("DB_NAME", "SmartAttendanceDB"),
        db_driver=os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server"),
        db_use_windows_auth=_as_bool(os.getenv("DB_USE_WINDOWS_AUTH"), True),
        db_username=os.getenv("DB_USERNAME", ""),
        db_password=os.getenv("DB_PASSWORD", ""),
        face_match_threshold=_as_float(os.getenv("FACE_MATCH_THRESHOLD"), 0.62),
        duplicate_cooldown_seconds=_as_int(os.getenv("DUPLICATE_COOLDOWN_SECONDS"), 120),
        unknown_alert_cooldown_seconds=_as_int(os.getenv("UNKNOWN_ALERT_COOLDOWN_SECONDS"), 300),
        yolo_face_model=os.getenv("YOLO_FACE_MODEL", "models/yolo/yolov8n-face.pt"),
        yolo_fallback_model=os.getenv("YOLO_FALLBACK_MODEL", "yolov8n.pt"),
        embeddings_path=os.getenv("EMBEDDINGS_PATH", "models/embeddings/facenet_embeddings.pkl"),
        known_faces_dir=os.getenv("KNOWN_FACES_DIR", "data/known_faces"),
        smtp_enabled=_as_bool(os.getenv("SMTP_ENABLED"), True),
        smtp_server=os.getenv("SMTP_SERVER", "smtp.gmail.com"),
        smtp_port=_as_int(os.getenv("SMTP_PORT"), 587),
        smtp_username=os.getenv("SMTP_USERNAME", ""),
        smtp_password=os.getenv("SMTP_PASSWORD", ""),
        alert_email_recipients=_as_list(os.getenv("ALERT_EMAIL_RECIPIENTS")),
        twilio_enabled=_as_bool(os.getenv("TWILIO_ENABLED"), False),
        twilio_account_sid=os.getenv("TWILIO_ACCOUNT_SID", ""),
        twilio_auth_token=os.getenv("TWILIO_AUTH_TOKEN", ""),
        twilio_from_number=os.getenv("TWILIO_FROM_NUMBER", ""),
        twilio_to_numbers=_as_list(os.getenv("TWILIO_TO_NUMBERS")),
        admin_username=os.getenv("ADMIN_USERNAME", "admin"),
        admin_password=os.getenv("ADMIN_PASSWORD", "Admin@123"),
        hr_username=os.getenv("HR_USERNAME", "hr"),
        hr_password=os.getenv("HR_PASSWORD", "Hr@123"),
        viewer_username=os.getenv("VIEWER_USERNAME", "viewer"),
        viewer_password=os.getenv("VIEWER_PASSWORD", "Viewer@123"),
    )

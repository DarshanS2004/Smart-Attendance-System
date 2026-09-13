from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.auth.security import hash_password
from src.config import ROOT_DIR, Settings, get_settings
from src.database.models import Base, SystemUser
from src.utils.logging import get_logger


logger = get_logger(__name__)


class DatabaseManager:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.engine = create_engine(
            self.settings.sqlalchemy_url(),
            echo=False,
            future=True,
            pool_pre_ping=True,
        )
        self._session_factory = sessionmaker(bind=self.engine, expire_on_commit=False, class_=Session)

    @contextmanager
    def session_scope(self) -> Session:
        session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def create_database_if_missing(self) -> None:
        connection_string = self.settings.pyodbc_connection_string("master")
        with pyodbc.connect(connection_string, autocommit=True) as connection:
            cursor = connection.cursor()
            cursor.execute(
                f"IF DB_ID(N'{self.settings.db_name}') IS NULL CREATE DATABASE [{self.settings.db_name}]"
            )
            cursor.close()

    def bootstrap(self) -> None:
        Path(ROOT_DIR / "data" / "exports").mkdir(parents=True, exist_ok=True)
        Path(ROOT_DIR / "data" / "logs").mkdir(parents=True, exist_ok=True)
        Path(self.settings.known_faces_full_path).mkdir(parents=True, exist_ok=True)
        Path(self.settings.embeddings_full_path).parent.mkdir(parents=True, exist_ok=True)
        self.create_database_if_missing()
        Base.metadata.create_all(self.engine)
        self.seed_default_users()

    def test_connection(self) -> bool:
        with self.engine.connect() as connection:
            connection.exec_driver_sql("SELECT 1")
        return True

    def seed_default_users(self) -> None:
        accounts = [
            (self.settings.admin_username, self.settings.admin_password, "admin"),
            (self.settings.hr_username, self.settings.hr_password, "hr"),
            (self.settings.viewer_username, self.settings.viewer_password, "viewer"),
        ]

        with self.session_scope() as session:
            for username, password, role in accounts:
                existing = session.query(SystemUser).filter(SystemUser.username == username).one_or_none()
                if existing:
                    continue
                session.add(
                    SystemUser(
                        username=username,
                        password_hash=hash_password(password),
                        role=role,
                        is_active=True,
                        created_at=datetime.utcnow(),
                    )
                )
        logger.info("Database bootstrap completed.")


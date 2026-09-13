from __future__ import annotations

import sys
from pathlib import Path

import cv2

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.config import get_settings
from src.database.db import DatabaseManager


def main() -> None:
    settings = get_settings()
    print(f"Application: {settings.app_name}")
    print(f"SQL Server: {settings.db_server} | Database: {settings.db_name}")
    print(f"Known faces directory: {settings.known_faces_full_path}")
    print(f"Embeddings file: {settings.embeddings_full_path}")
    print(f"YOLO model exists: {settings.yolo_face_model_full_path.exists()}")

    try:
        database = DatabaseManager(settings)
        database.bootstrap()
        print("Database connection: OK" if database.test_connection() else "Database connection: FAILED")
    except Exception as exc:
        print(f"Database connection: FAILED -> {exc}")
        print("Hint: if SQLEXPRESS uses a dynamic port, start SQL Browser or update `.env` to the active TCP port.")

    camera = cv2.VideoCapture(settings.camera_index)
    is_open = camera.isOpened()
    print(f"Camera open: {is_open}")
    camera.release()


if __name__ == "__main__":
    main()

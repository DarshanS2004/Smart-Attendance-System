from __future__ import annotations

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.config import get_settings
from src.database.db import DatabaseManager
from src.database.repository import AttendanceRepository
from src.recognition.facenet_recognizer import FaceNetRecognizer


def main() -> None:
    settings = get_settings()
    database = DatabaseManager(settings)
    database.bootstrap()
    repository = AttendanceRepository(database)
    recognizer = FaceNetRecognizer(repository, settings)
    enrolled = recognizer.enroll_from_directory()
    if not enrolled:
        print("No people were enrolled. Add folders in data/known_faces and try again.")
        return

    print("Enrollment completed:")
    for row in enrolled:
        print(f"- {row['employee_code']} | {row['full_name']} | images={row['image_count']}")


if __name__ == "__main__":
    main()

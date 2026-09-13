from __future__ import annotations

from src.core.pipeline import AttendancePipeline


def main() -> None:
    try:
        pipeline = AttendancePipeline()
        pipeline.run(show_window=True)
    except Exception as exc:
        print("Camera pipeline failed to start.")
        print(str(exc))
        print("Check SQL Server connectivity, webcam access, and Python dependencies in the virtual environment.")


if __name__ == "__main__":
    main()

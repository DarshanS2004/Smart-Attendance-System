from __future__ import annotations

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.config import get_settings
from src.database.db import DatabaseManager


def main() -> None:
    settings = get_settings()
    try:
        database = DatabaseManager(settings)
        database.bootstrap()
        database.test_connection()
        print(f"Database '{settings.db_name}' is ready on {settings.db_server}.")
    except Exception as exc:
        print("Database bootstrap failed.")
        print(str(exc))
        print("Tips:")
        print("- Confirm the SQLEXPRESS service is running.")
        print("- If SQL Browser is stopped, use the actual SQL TCP port in `.env` or start SQL Browser.")
        print("- If ODBC Driver 17 fails, switch `DB_DRIVER` to `ODBC Driver 18 for SQL Server`.")
        raise


if __name__ == "__main__":
    main()

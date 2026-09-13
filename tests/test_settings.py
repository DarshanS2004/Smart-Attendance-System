from src.config import get_settings


def test_settings_load_defaults() -> None:
    settings = get_settings()
    assert settings.app_name == "Smart Attendance System"
    assert settings.db_name == "SmartAttendanceDB"
    assert settings.camera_index == 0


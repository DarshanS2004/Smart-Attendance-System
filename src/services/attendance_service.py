from __future__ import annotations

from datetime import datetime

from src.alerts.notifier import Notifier
from src.config import Settings, get_settings
from src.database.repository import AttendanceRepository


class AttendanceService:
    def __init__(
        self,
        repository: AttendanceRepository,
        notifier: Notifier,
        settings: Settings | None = None,
    ) -> None:
        self.repository = repository
        self.notifier = notifier
        self.settings = settings or get_settings()
        self.marked_today: set[tuple[int, str]] = set()
        self.last_unknown_alert_at: datetime | None = None

    def handle_recognition(
        self,
        recognition: dict,
        track_id: str,
        camera_source: str,
        frame_path: str | None = None,
    ) -> dict:
        detected_at = datetime.utcnow()
        if recognition["matched"]:
            person_id = int(recognition["person_id"])
            cache_key = (person_id, detected_at.date().isoformat())

            if cache_key in self.marked_today:
                return {
                    "created": False,
                    "is_duplicate": True,
                    "attendance_already_marked": True,
                }

            if self.repository.attendance_exists_for_date(person_id, detected_at.date()):
                self.marked_today.add(cache_key)
                return {
                    "created": False,
                    "is_duplicate": True,
                    "attendance_already_marked": True,
                }

            result = self.repository.mark_attendance(
                person_id=person_id,
                track_id=track_id,
                confidence=recognition["confidence"],
                camera_source=camera_source,
                label=recognition["label"],
                is_duplicate=False,
                frame_path=frame_path,
                detected_at=detected_at,
            )
            self.marked_today.add(cache_key)
            return result

        self.repository.log_unknown_event(
            track_id=track_id,
            confidence=recognition["confidence"],
            camera_source=camera_source,
            label=recognition["label"],
            frame_path=frame_path,
            detected_at=detected_at,
        )

        should_alert = (
            self.last_unknown_alert_at is None
            or (detected_at - self.last_unknown_alert_at).total_seconds()
            >= self.settings.unknown_alert_cooldown_seconds
        )
        if should_alert:
            message = (
                f"Unknown face detected at {detected_at:%Y-%m-%d %H:%M:%S} "
                f"from camera source {camera_source}."
            )
            email_ok, email_state = self.notifier.send_email(
                subject="Smart Attendance Alert: Unknown Face",
                body=message,
            )
            sms_ok, sms_state = self.notifier.send_sms(message)
            if email_ok:
                self.repository.log_alert("EMAIL", message, ",".join(self.settings.alert_email_recipients), "sent")
            elif self.settings.alert_email_recipients:
                self.repository.log_alert("EMAIL", email_state, ",".join(self.settings.alert_email_recipients), "failed")

            if sms_ok:
                self.repository.log_alert("SMS", message, ",".join(self.settings.twilio_to_numbers), "sent")
            elif self.settings.twilio_to_numbers:
                self.repository.log_alert("SMS", sms_state, ",".join(self.settings.twilio_to_numbers), "failed")
            self.last_unknown_alert_at = detected_at

        return {"created": False, "is_duplicate": False}

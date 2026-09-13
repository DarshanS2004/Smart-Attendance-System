from __future__ import annotations

from datetime import date, datetime, timedelta

from sqlalchemy import desc, func
from sqlalchemy.orm import joinedload

from src.auth.security import verify_password
from src.database.db import DatabaseManager
from src.database.models import AlertLog, Attendance, AttendanceEvent, Person, SystemUser


class AttendanceRepository:
    def __init__(self, db: DatabaseManager) -> None:
        self.db = db

    def authenticate_user(self, username: str, password: str) -> dict | None:
        with self.db.session_scope() as session:
            user = session.query(SystemUser).filter(SystemUser.username == username).one_or_none()
            if not user or not user.is_active:
                return None
            if not verify_password(password, user.password_hash):
                return None
            return {
                "id": user.id,
                "username": user.username,
                "role": user.role,
            }

    def upsert_person(self, profile: dict, image_dir: str | None = None) -> Person:
        with self.db.session_scope() as session:
            person = (
                session.query(Person)
                .filter(Person.employee_code == profile["employee_code"])
                .one_or_none()
            )
            if not person:
                person = Person(
                    employee_code=profile["employee_code"],
                    full_name=profile["full_name"],
                    department=profile.get("department"),
                    email=profile.get("email"),
                    phone=profile.get("phone"),
                    image_dir=image_dir,
                    is_active=True,
                )
                session.add(person)
                session.flush()
                session.refresh(person)
                return person

            person.full_name = profile["full_name"]
            person.department = profile.get("department")
            person.email = profile.get("email")
            person.phone = profile.get("phone")
            person.image_dir = image_dir or person.image_dir
            session.flush()
            session.refresh(person)
            return person

    def list_people(self) -> list[dict]:
        with self.db.session_scope() as session:
            people = session.query(Person).order_by(Person.full_name.asc()).all()
            return [
                {
                    "id": person.id,
                    "employee_code": person.employee_code,
                    "full_name": person.full_name,
                    "department": person.department or "Unassigned",
                    "email": person.email or "",
                    "phone": person.phone or "",
                    "image_dir": person.image_dir or "",
                    "is_active": person.is_active,
                    "created_at": person.created_at,
                }
                for person in people
            ]

    def mark_attendance(
        self,
        person_id: int,
        track_id: str,
        confidence: float,
        camera_source: str,
        label: str,
        is_duplicate: bool,
        frame_path: str | None = None,
        detected_at: datetime | None = None,
    ) -> dict:
        detected_at = detected_at or datetime.utcnow()
        with self.db.session_scope() as session:
            attendance = (
                session.query(Attendance)
                .filter(
                    Attendance.person_id == person_id,
                    Attendance.attendance_date == detected_at.date(),
                )
                .one_or_none()
            )
            created = attendance is None
            if created:
                attendance = Attendance(
                    person_id=person_id,
                    attendance_date=detected_at.date(),
                    first_seen_at=detected_at,
                    last_seen_at=detected_at,
                    total_detections=1,
                    camera_source=camera_source,
                    status="present",
                )
                session.add(attendance)
            else:
                attendance.last_seen_at = detected_at
                attendance.total_detections += 1

            event = AttendanceEvent(
                person_id=person_id,
                track_id=str(track_id),
                confidence=float(confidence),
                detected_at=detected_at,
                camera_source=camera_source,
                label=label,
                is_duplicate=is_duplicate,
                frame_path=frame_path,
            )
            session.add(event)
            session.flush()
            return {
                "created": created,
                "is_duplicate": is_duplicate,
                "attendance_id": attendance.id,
                "event_id": event.id,
            }

    def attendance_exists_for_date(self, person_id: int, attendance_date: date) -> bool:
        with self.db.session_scope() as session:
            attendance = (
                session.query(Attendance.id)
                .filter(
                    Attendance.person_id == person_id,
                    Attendance.attendance_date == attendance_date,
                )
                .first()
            )
            return attendance is not None

    def log_unknown_event(
        self,
        track_id: str,
        confidence: float,
        camera_source: str,
        label: str,
        frame_path: str | None = None,
        detected_at: datetime | None = None,
    ) -> None:
        detected_at = detected_at or datetime.utcnow()
        with self.db.session_scope() as session:
            session.add(
                AttendanceEvent(
                    person_id=None,
                    track_id=str(track_id),
                    confidence=float(confidence),
                    detected_at=detected_at,
                    camera_source=camera_source,
                    label=label,
                    is_duplicate=False,
                    frame_path=frame_path,
                )
            )

    def log_alert(
        self,
        alert_type: str,
        message: str,
        recipient: str | None,
        status: str,
        person_id: int | None = None,
    ) -> None:
        with self.db.session_scope() as session:
            session.add(
                AlertLog(
                    person_id=person_id,
                    alert_type=alert_type,
                    message=message,
                    recipient=recipient,
                    status=status,
                )
            )

    def get_recent_events(self, limit: int = 20) -> list[dict]:
        with self.db.session_scope() as session:
            rows = (
                session.query(AttendanceEvent)
                .options(joinedload(AttendanceEvent.person))
                .order_by(desc(AttendanceEvent.detected_at))
                .limit(limit)
                .all()
            )
            return [
                {
                    "time": row.detected_at,
                    "person": row.person.full_name if row.person else row.label,
                    "employee_code": row.person.employee_code if row.person else "UNKNOWN",
                    "track_id": row.track_id,
                    "confidence": round(row.confidence, 3),
                    "camera_source": row.camera_source,
                    "duplicate": row.is_duplicate,
                }
                for row in rows
            ]

    def get_alert_logs(self, limit: int = 20) -> list[dict]:
        with self.db.session_scope() as session:
            rows = session.query(AlertLog).order_by(desc(AlertLog.sent_at)).limit(limit).all()
            return [
                {
                    "time": row.sent_at,
                    "type": row.alert_type,
                    "message": row.message,
                    "recipient": row.recipient or "",
                    "status": row.status,
                }
                for row in rows
            ]

    def get_overview_metrics(self) -> dict:
        today = date.today()
        start_of_month = today.replace(day=1)
        with self.db.session_scope() as session:
            registered_people = session.query(func.count(Person.id)).scalar() or 0
            today_present = (
                session.query(func.count(Attendance.id))
                .filter(Attendance.attendance_date == today)
                .scalar()
                or 0
            )
            month_present = (
                session.query(func.count(Attendance.id))
                .filter(Attendance.attendance_date >= start_of_month)
                .scalar()
                or 0
            )
            unknown_faces = (
                session.query(func.count(AttendanceEvent.id))
                .filter(
                    AttendanceEvent.person_id.is_(None),
                    AttendanceEvent.detected_at >= datetime.combine(today, datetime.min.time()),
                )
                .scalar()
                or 0
            )
            return {
                "registered_people": registered_people,
                "today_present": today_present,
                "month_present": month_present,
                "unknown_faces": unknown_faces,
            }

    def get_daily_attendance(self, days: int = 7) -> list[dict]:
        start_date = date.today() - timedelta(days=days - 1)
        with self.db.session_scope() as session:
            rows = (
                session.query(Attendance.attendance_date, func.count(Attendance.id))
                .filter(Attendance.attendance_date >= start_date)
                .group_by(Attendance.attendance_date)
                .order_by(Attendance.attendance_date.asc())
                .all()
            )
            return [{"date": row[0], "count": row[1]} for row in rows]

    def get_monthly_attendance(self, months: int = 6) -> list[dict]:
        start_date = date.today() - timedelta(days=31 * (months - 1))
        with self.db.session_scope() as session:
            rows = (
                session.query(
                    func.year(Attendance.attendance_date).label("year"),
                    func.month(Attendance.attendance_date).label("month"),
                    func.count(Attendance.id).label("count"),
                )
                .filter(Attendance.attendance_date >= start_date)
                .group_by(func.year(Attendance.attendance_date), func.month(Attendance.attendance_date))
                .order_by(func.year(Attendance.attendance_date), func.month(Attendance.attendance_date))
                .all()
            )
            return [
                {
                    "month": f"{row.year}-{row.month:02d}",
                    "count": row.count,
                }
                for row in rows
            ]

    def get_person_wise_counts(self, limit: int = 15) -> list[dict]:
        with self.db.session_scope() as session:
            rows = (
                session.query(
                    Person.full_name,
                    Person.employee_code,
                    func.count(Attendance.id).label("attendance_count"),
                )
                .join(Attendance, Attendance.person_id == Person.id, isouter=True)
                .group_by(Person.full_name, Person.employee_code)
                .order_by(func.count(Attendance.id).desc(), Person.full_name.asc())
                .limit(limit)
                .all()
            )
            return [
                {
                    "full_name": row.full_name,
                    "employee_code": row.employee_code,
                    "attendance_count": row.attendance_count,
                }
                for row in rows
            ]

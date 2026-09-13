from __future__ import annotations

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.config import Settings, get_settings
from src.utils.logging import get_logger


logger = get_logger(__name__)


class Notifier:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self._twilio_client = None
        if self.settings.twilio_enabled:
            try:
                from twilio.rest import Client

                self._twilio_client = Client(
                    self.settings.twilio_account_sid,
                    self.settings.twilio_auth_token,
                )
            except Exception as exc:
                logger.warning("Twilio client not available: %s", exc)

    def send_email(self, subject: str, body: str, recipients: list[str] | None = None) -> tuple[bool, str]:
        recipients = recipients or self.settings.alert_email_recipients
        if not self.settings.smtp_enabled or not recipients:
            return False, "Email alerts disabled or recipients missing."

        message = MIMEMultipart()
        message["From"] = self.settings.smtp_username
        message["To"] = ", ".join(recipients)
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP(self.settings.smtp_server, self.settings.smtp_port) as server:
                server.starttls()
                server.login(self.settings.smtp_username, self.settings.smtp_password)
                server.sendmail(self.settings.smtp_username, recipients, message.as_string())
            return True, "Email sent."
        except Exception as exc:
            logger.exception("Email sending failed")
            return False, str(exc)

    def send_sms(self, body: str, recipients: list[str] | None = None) -> tuple[bool, str]:
        recipients = recipients or self.settings.twilio_to_numbers
        if not self.settings.twilio_enabled or not recipients or not self._twilio_client:
            return False, "SMS alerts disabled or recipients missing."

        try:
            for recipient in recipients:
                self._twilio_client.messages.create(
                    body=body,
                    from_=self.settings.twilio_from_number,
                    to=recipient,
                )
            return True, "SMS sent."
        except Exception as exc:
            logger.exception("SMS sending failed")
            return False, str(exc)


from __future__ import annotations

from datetime import datetime, timezone
import logging

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client as TwilioClient

from app.config.app_config import settings
from app.notification.domain.entities.models import Notification

logger = logging.getLogger("app")


class SmsMessageService:
    def __init__(self, client: TwilioClient | None = None) -> None:
        self.client = client
        if self.client is None and settings.TWILIO_ENABLED:
            self.client = TwilioClient(
                settings.TWILIO_ACCOUNT_SID,
                settings.TWILIO_AUTH_TOKEN,
            )

    async def send(self, notification: Notification) -> None:
        phone_number = notification.recipient.phone_number
        if not phone_number:
            raise ValueError("Recipient phone_number is required.")
        if not settings.TWILIO_ENABLED:
            logger.info(
                "sms.noop notification_id=%s phone=%s",
                notification.notification_id,
                self._mask_phone(phone_number),
            )
            return
        if self.client is None:
            raise RuntimeError("Twilio client is not configured.")
        try:
            message = self.client.messages.create(
                to=phone_number,
                from_=settings.TWILIO_PHONE_NUMBER,
                body=notification.content.body,
            )
            logger.info(
                "sms.sent notification_id=%s sid=%s timestamp=%s",
                notification.notification_id,
                getattr(message, "sid", "unknown"),
                datetime.now(timezone.utc).isoformat(),
            )
        except TwilioRestException:
            logger.exception("sms.twilio_error notification_id=%s", notification.notification_id)
            raise

    @staticmethod
    def _mask_phone(phone_number: str) -> str:
        if len(phone_number) <= 4:
            return "****"
        return f"{phone_number[:2]}***{phone_number[-2:]}"

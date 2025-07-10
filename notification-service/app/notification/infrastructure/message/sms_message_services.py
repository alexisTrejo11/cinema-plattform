from twilio.rest import Client as TwilioClient
from twilio.base.exceptions import TwilioRestException
from config.app_config import settings
from typing import Dict, Any
from app.notification.domain.entities.content import NotificationContent
from app.notification.domain.entities.models import Notification
from app.notification.domain.enums import NotificationChannel, NotificationStatus
from datetime import datetime


class SmsMessageService:
    def __init__(self, client: TwilioClient) -> None:
        self.client = client
        self.max_retries = 3
        self.timeout_secs = 10

    async def send(self, notification: Notification):
        if not notification.recipient.phone_number:
            raise ValueError("Phone Number is Required")

        result = self.send_notification(
            phone_number=notification.recipient.phone_number,
            content=notification.content,
            notification_id=notification.notification_id,
        )

        if result["error"]:
            raise ValueError(f"error ocurred sending sms: {result['error']}")

        import logging

        logger = logging.getLogger("app")
        logger.info(
            f"sms send it for nottification {result['notification_id']} timestamp {result['sent_at']}"
        )

    def send_notification(
        self, phone_number: str, content: NotificationContent, notification_id: str
    ) -> Dict[str, Any]:
        result = {
            "notification_id": notification_id,
            "channel": NotificationChannel.SMS.value,
            "status": NotificationStatus.FAILED.value,
            "sent_at": None,
            "error": None,
            "provider_response": None,
        }
        try:
            if not self._validate_phone_number(phone_number):
                raise ValueError("Invalid Phone Number")

            for attempt in range(self.max_retries):
                try:
                    message = self.client.messages.create(
                        to=phone_number,
                        from_=settings.twilio_phone_number,
                        body=content.body,
                        # status_callback=f"{settings.api_base_url}/notifications/callback/{notification_id}",
                        # timeout=self.timeout,
                    )

                    result.update(
                        {
                            "status": NotificationStatus.SENT.value,
                            "sent_at": datetime.utcnow().isoformat(),
                            "provider_response": message.sid,
                        }
                    )
                    return result

                except TwilioRestException as e:
                    if attempt == self.max_retries - 1:
                        raise
                    continue

        except TwilioRestException as e:
            result["error"] = f"Twilio error: {str(e)}"
            result["provider_response"] = getattr(e, "msg", str(e))
        except Exception as e:
            result["error"] = f"Unexpected error: {str(e)}"

        return result

    def _validate_phone_number(self, phone_number: str) -> bool:
        return phone_number.startswith("+") and len(phone_number) > 8

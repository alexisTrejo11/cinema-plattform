from twilio.rest import Client as TwilioClient
from twilio.base.exceptions import TwilioRestException
from config.app_config import settings
from typing import Dict, Any
from app.notification.domain.entities.content import NotificationContent
from app.notification.domain.enums import NotificationChannel, NotificationStatus
from datetime import datetime


class SmsMessageService:
    def __init__(self, client: TwilioClient) -> None:
        self.client = client
        self.max_retries = 3
        self.timeout_secs = 10

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
                        from_=settings.twilio_number,
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

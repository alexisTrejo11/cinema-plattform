from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from typing import Any, Dict, List

import logging
from jinja2 import Template

from app.config.app_config import settings
from app.notification.domain.entities.models import Notification
from app.notification.domain.enums import NotificationType
from app.notification.infrastructure.email.html_teamplates import (
    AUTH_CODE_TEMPLATE,
    GENERIC_INFO_TEMPLATE,
    TICKET_PURCHASE_TEMPLATE,
    USER_ACTIVATION_TEMPLATE,
)


logger = logging.getLogger(__name__)


class EmailService:
    async def send(self, notification: Notification) -> None:
        if not notification.recipient.email:
            raise ValueError("Recipient email is required.")
        template_data = notification.content.data or {}
        html_content = self._render_template(
            notification_type=notification.notification_type,
            template_data=template_data,
        )
        attachments = template_data.get("attachments", [])
        self._send_email(
            to_email=notification.recipient.email,
            subject=notification.content.subject,
            html_content=html_content,
            attachments=attachments if isinstance(attachments, list) else [],
        )

    def _send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        attachments: List[dict[str, Any]],
    ) -> None:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = (
                f"{settings.EMAIL_FROM_NAME} <{settings.EMAIL_FROM_ADDRESS}>"
            )
            msg["To"] = to_email
            msg.attach(MIMEText(html_content, "html"))
            self._attach_files(msg, attachments)

            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                if settings.SMTP_USE_TLS:
                    server.starttls()
                if settings.SMTP_USERNAME:
                    server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                server.send_message(msg)
            logger.info("email.sent to=%s", to_email)
        except Exception:
            logger.exception("email.send_failed to=%s", to_email)
            raise

    def _render_template(
        self, notification_type: NotificationType, template_data: Dict[str, Any]
    ) -> str:
        template_content = self._resolve_template(notification_type)
        return Template(template_content).render(**template_data)

    def _resolve_template(self, notification_type: NotificationType) -> str:
        templates = {
            NotificationType.TICKET_BUY: TICKET_PURCHASE_TEMPLATE,
            NotificationType.ACCOUNT_CREATED: USER_ACTIVATION_TEMPLATE,
            NotificationType.ACCOUNT_AUTH: AUTH_CODE_TEMPLATE,
            NotificationType.ANNOUNCEMENT: GENERIC_INFO_TEMPLATE,
            NotificationType.CUSTOM_MESSAGE: GENERIC_INFO_TEMPLATE,
            NotificationType.PAYMENT_FAILED: GENERIC_INFO_TEMPLATE,
            NotificationType.PRODUCT_BUY: GENERIC_INFO_TEMPLATE,
            NotificationType.ACCOUNT_DELETED: GENERIC_INFO_TEMPLATE,
        }
        return templates.get(notification_type, GENERIC_INFO_TEMPLATE)

    def _attach_files(
        self, message: MIMEMultipart, attachments: List[dict[str, Any]]
    ) -> None:
        for attachment in attachments:
            content = attachment.get("content")
            if content is None:
                continue
            file_name = attachment.get("filename", "attachment.pdf")
            content_type = attachment.get("content_type", "application/pdf")
            if isinstance(content, str):
                binary = content.encode("utf-8")
            else:
                binary = content
            try:
                part = MIMEApplication(binary, _subtype=content_type.split("/")[-1])
                part.add_header("Content-Disposition", "attachment", filename=file_name)
                message.attach(part)
            except Exception:
                logger.warning("email.attachment_skipped filename=%s", file_name)

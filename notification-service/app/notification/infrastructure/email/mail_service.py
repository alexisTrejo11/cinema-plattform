from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from typing import Dict, Any, Optional
from jinja2 import Template
import logging
from config.app_config import EmailConfig
from .html_teamplates import *

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self, config: EmailConfig) -> None:
        self.config = config

    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        from_email: Optional[str] = None,
        from_name: Optional[str] = None,
    ) -> bool:
        """
        Send an HTML email.

        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML content of the email
            from_email: Sender email (optional)
            from_name: Sender name (optional)

        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = (
                f"{from_name or self.config.from_name} <{from_email or self.config.from_email}>"
            )
            msg["To"] = to_email

            # Add HTML content
            html_part = MIMEText(html_content, "html")
            msg.attach(html_part)

            # Send email
            with smtplib.SMTP(self.config.smtp_server, self.config.smtp_port) as server:
                server.starttls()
                server.login(self.config.smtp_username, self.config.smtp_password)
                server.send_message(msg)

            logger.info(f"Email sent successfully to {to_email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False

    def send_template_email(
        self,
        to_email: str,
        template_name: str,
        subject: str,
        template_data: Dict[str, Any],
        from_email: Optional[str] = None,
        from_name: Optional[str] = None,
    ) -> bool:
        """
        Send an email using a template.

        Args:
            to_email: Recipient email address
            template_name: Name of the template to use
            subject: Email subject
            template_data: Data to populate the template
            from_email: Sender email (optional)
            from_name: Sender name (optional)

        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        try:
            # Get template
            template_content = self.get_template(template_name)
            if not template_content:
                logger.error(f"Template {template_name} not found")
                return False

            # Render template
            template = Template(template_content)
            html_content = template.render(**template_data)

            # Send email
            return self.send_email(
                to_email=to_email,
                subject=subject,
                html_content=html_content,
                from_email=from_email,
                from_name=from_name,
            )

        except Exception as e:
            logger.error(f"Failed to send template email to {to_email}: {str(e)}")
            return False

    def get_template(self, template_name: str) -> Optional[str]:
        """
        Get email template content.
        """

        templates = {
            "ticket_purchase": TICKET_PURCHASE_TEMPLATE,
            "account_created": ACCOUNT_CREATED_TEMPLATE,
            "auth_code": AUTH_CODE_TEMPLATE,
            "announcement": ANNOUNCEMENT_TEMPLATE,
            "payment_failed": PAYMENT_FAILED_TEMPLATE,
        }
        return templates.get(template_name)

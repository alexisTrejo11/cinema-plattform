import logging

from app.notification.application.commands.notification_command import (
    ProcessIncomingNotificationEventCommand,
)

logger = logging.getLogger("app")


class ProcessIncomingNotificationEventUseCase:
    """
    Reserved use case for future Kafka-driven event orchestration.
    Implement event_type routing when cross-service contracts are available.
    """

    async def execute(self, command: ProcessIncomingNotificationEventCommand) -> None:
        logger.info(
            "incoming_notification_event.placeholder event_type=%s event_id=%s",
            command.event_type,
            command.event_id,
        )

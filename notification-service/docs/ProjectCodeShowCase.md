# Code Showcase

## Code Examples (`CodeExample[]`)

### Example 1 (`CodeExample`)

- **ID**: notification-aggregate
- **Title**: Notification Domain Aggregate
- **Description**: The core Notification aggregate root with lifecycle state management (PENDING → SENT/FAILED) and attention tracking
- **Category**: domain
- **Duration** (optional): 
- **Views** (optional): 
- **Tags** (optional):
  - ddd
  - aggregate
  - domain
  - pydantic

#### Files (`CodeFile[]`)

- **Name**: models.py
- **Path**: app/notification/domain/entities/models.py
- **Language**: python
- **Content**:
  ```python
  from __future__ import annotations

  from datetime import datetime, timezone
  from typing import Any, Dict, Optional
  from uuid import uuid4

  from pydantic import BaseModel, ConfigDict, Field, model_validator

  from ..enums import (
      NotificationAttentionStatus,
      NotificationChannel,
      NotificationStatus,
      NotificationType,
  )
  from .content import NotificationContent
  from .recipient import Recipient


  class Notification(BaseModel):
      """Domain aggregate for a notification lifecycle."""

      model_config = ConfigDict(validate_assignment=True)

      notification_id: str = Field(default_factory=lambda: str(uuid4()))
      notification_type: NotificationType
      recipient: Recipient
      content: NotificationContent
      channel: NotificationChannel
      created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
      event_id: Optional[str] = None
      status: NotificationStatus = NotificationStatus.PENDING
      sent_at: Optional[datetime] = None
      failed_at: Optional[datetime] = None
      error_details: Optional[str] = None
      provider_response: Optional[str] = None
      source: Optional[str] = None
      source_event_type: Optional[str] = None
      correlation_id: Optional[str] = None
      causation_id: Optional[str] = None
      is_important: bool = False
      attention_status: NotificationAttentionStatus = NotificationAttentionStatus.NONE
      metadata: Dict[str, Any] = Field(default_factory=dict)

      def mark_as_sent(self, sent_at: Optional[datetime] = None) -> None:
          self.status = NotificationStatus.SENT
          self.sent_at = sent_at or datetime.now(timezone.utc)
          self.failed_at = None
          self.error_details = None

      def mark_as_failed(
          self,
          error_details: str,
          failed_at: Optional[datetime] = None,
          provider_response: Optional[str] = None,
      ) -> None:
          self.status = NotificationStatus.FAILED
          self.failed_at = failed_at or datetime.now(timezone.utc)
          self.error_details = error_details
          self.provider_response = provider_response
          self.sent_at = None

      def mark_attention_open(self) -> None:
          self.is_important = True
          self.attention_status = NotificationAttentionStatus.OPEN
  ```
- **Highlighted** (optional): `true`
- **Explanation** (optional): The Notification aggregate encapsulates all state transitions and business rules for the notification lifecycle.

---

### Example 2 (`CodeExample`)

- **ID**: event-routing
- **Title**: Kafka Event Processing and Routing
- **Description**: ProcessIncomingNotificationEventUseCase handles Kafka event consumption with deduplication, recipient resolution, and automatic routing based on event type
- **Category**: application
- **Duration** (optional): 
- **Views** (optional): 
- **Tags** (optional):
  - kafka
  - event-driven
  - deduplication
  - routing

#### Files (`CodeFile[]`)

- **Name**: incoming_event_usecases.py
- **Path**: app/notification/application/usecases/incoming_event_usecases.py
- **Language**: python
- **Content**:
  ```python
  IMPORTANT_EVENT_KEYWORDS = ("failed", "deleted", "banned", "fraud", "chargeback", "alert")
  IMPORTANT_EVENT_TYPES = {
      "user.lifecycle.deleted",
      "user.lifecycle.banned",
      "payment.failed",
      "wallet.payment_failed",
  }
  STORE_ONLY_EVENT_TYPES = {
      "user.lifecycle.deleted",
  }


  class ProcessIncomingNotificationEventUseCase:
      """Routes Kafka incoming events into local notifications + optional delivery."""

      def __init__(
          self,
          repository: NotificationRepository,
          sending_service: SendingService,
          user_profile_service: UserProfileService | None = None,
      ) -> None:
          self._repository = repository
          self._sending_service = sending_service
          self._user_profile_service = user_profile_service

      async def execute(self, command: ProcessIncomingNotificationEventCommand) -> None:
          existing = await self._repository.get_by_event_id(command.event_id)
          if existing is not None:
              logger.info("duplicate_skipped event_id=%s", command.event_id)
              return

          payload = command.payload or {}
          recipient = await self._resolve_recipient(payload)
          decision = self._route_event(command.event_type, payload)

          notification = Notification(
              notification_type=decision.notification_type,
              recipient=recipient,
              content=NotificationContent(
                  subject=decision.subject,
                  body=decision.body,
                  data=decision.payload_data,
              ),
              channel=decision.channel,
              event_id=command.event_id,
              source=command.source,
              is_important=decision.is_important,
              attention_status=(
                  NotificationAttentionStatus.OPEN
                  if decision.is_important
                  else NotificationAttentionStatus.NONE
              ),
          )

          saved = await self._repository.save(notification)
          # ... send if needed
  ```
- **Highlighted** (optional): `true`
- **Explanation** (optional): This use case demonstrates event deduplication, importance detection, and automatic routing based on event types.

---

### Example 3 (`CodeExample`)

- **ID**: multi-channel-delivery
- **Title**: Multi-Channel Sending Service
- **Description**: SendingServiceImplementation routes notifications to the appropriate channel adapter (EmailService or SmsMessageService)
- **Category**: infrastructure
- **Duration** (optional): 
- **Views** (optional): 
- **Tags** (optional):
  - adapter
  - strategy
  - routing

#### Files (`CodeFile[]`)

- **Name**: services.py
- **Path**: app/notification/infrastructure/services.py
- **Language**: python
- **Content**:
  ```python
  from app.notification.domain.sending_service import SendingService
  from app.notification.domain.entities.models import Notification
  from app.notification.domain.enums import NotificationChannel
  from .email.mail_service import EmailService
  from .message.sms_message_services import SmsMessageService
  import logging

  logger = logging.getLogger("app")


  class SendingServiceImplementation(SendingService):
      def __init__(
          self, email_service: EmailService, sms_service: SmsMessageService
      ) -> None:
          self.email_service = email_service
          self.sms_service = sms_service

      async def send_notification(self, notification: Notification) -> None:
          match notification.channel:
              case NotificationChannel.EMAIL:
                  await self.email_service.send(notification)
              case NotificationChannel.SMS:
                  await self.sms_service.send(notification)
              case _:
                  logger.info(
                      "channel not yet implemented channel=%s",
                      notification.channel.value,
                  )
  ```
- **Highlighted** (optional): `false`
- **Explanation** (optional): Pattern matching for channel-based routing with extensible architecture for future channels.

---

### Example 4 (`CodeExample`)

- **ID**: email-templates
- **Title**: Jinja2 Email Templates
- **Description**: HTML email templates using Jinja2 for consistent branding and personalization
- **Category**: infrastructure
- **Duration** (optional): 
- **Views** (optional): 
- **Tags** (optional):
  - jinja2
  - email
  - templates
  - html

#### Files (`CodeFile[]`)

- **Name**: html_templates.py
- **Path**: app/notification/infrastructure/email/html_templates.py
- **Language**: html+jinja
- **Content**:
  ```html+jinja
  USER_ACTIVATION = """
  <!DOCTYPE html>
  <html>
  <head>
      <meta charset="utf-8">
      <title>Activate Your Account</title>
  </head>
  <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
      <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
          <h1 style="color: #4A90E2;">Welcome to Cinema Platform!</h1>
          <p>Hello {{ user_name }},</p>
          <p>Thank you for registering. Please click the button below to activate your account:</p>
          <a href="{{ activation_url }}" style="display: inline-block; padding: 12px 24px; 
             background-color: #4A90E2; color: white; text-decoration: none; border-radius: 4px;">
             Activate Account
          </a>
          <p style="margin-top: 20px; font-size: 12px; color: #666;">
             If you didn't create this account, please ignore this email.
          </p>
      </div>
  </body>
  </html>
  """

  AUTH_CODE = """
  <!DOCTYPE html>
  <html>
  <head>
      <meta charset="utf-8">
      <title>Your Authentication Code</title>
  </head>
  <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
      <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
          <h1 style="color: #4A90E2;">Your Verification Code</h1>
          <p>Hello {{ user_name }},</p>
          <div style="background-color: #f5f5f5; padding: 20px; text-align: center; 
                      font-size: 32px; letter-spacing: 8px; font-weight: bold;">
              {{ auth_code }}
          </div>
          <p style="margin-top: 20px;">This code will expire in {{ expiry_minutes }} minutes.</p>
      </div>
  </body>
  </html>
  """

  TICKET_PURCHASE = """
  <!DOCTYPE html>
  <html>
  <head>
      <meta charset="utf-8">
      <title>Ticket Confirmation</title>
  </head>
  <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
      <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
          <h1 style="color: #50C878;">🎬 Tickets Confirmed!</h1>
          <p>Hello {{ user_name }},</p>
          <p>Your tickets have been purchased successfully.</p>
          <div style="background-color: #f5f5f5; padding: 20px; border-radius: 8px;">
              <p><strong>Movie:</strong> {{ movie_title }}</p>
              <p><strong>Date:</strong> {{ show_date }}</p>
              <p><strong>Time:</strong> {{ show_time }}</p>
              <p><strong>Seats:</strong> {{ seats }}</p>
          </div>
          <p style="margin-top: 20px;">Show your QR code at the cinema entrance.</p>
      </div>
  </body>
  </html>
  """
  ```
- **Highlighted** (optional): `false`
- **Explanation** (optional): Responsive HTML email templates with consistent branding using Cinema Platform colors.

---

### Example 5 (`CodeExample`)

- **ID**: api-controller
- **Title**: FastAPI Notification Controller
- **Description**: REST API endpoints with dependency injection for use cases
- **Category**: presentation
- **Duration** (optional): 
- **Views** (optional): 
- **Tags** (optional):
  - fastapi
  - api
  - rest

#### Files (`CodeFile[]`)

- **Name**: notification_controller.py
- **Path**: app/notification/presentation/notification_controller.py
- **Language**: python
- **Content**:
  ```python
  from fastapi import APIRouter, Depends, HTTPException, Query, status

  from app.notification.application.commands.notification_command import (
      CreateNotificationCommand,
  )
  from app.notification.application.dtos import (
      NotificationListResponse,
      NotificationResponse,
  )
  from app.notification.application.queries.notification_queries import (
      GetNotificationByIdQuery,
      ListNotificationsQuery,
  )
  from app.notification.application.usecases.notification_usecases import (
      CreateNotificationUseCase,
      GetNotificationByIdUseCase,
      ListNotificationsUseCase,
  )
  from app.notification.domain.enums import (
      NotificationAttentionStatus,
      NotificationChannel,
      NotificationStatus,
      NotificationType,
  )

  from .dependencies import (
      get_create_notification_usecase,
      get_list_notifications_usecase,
      get_notification_by_id_usecase,
  )

  router = APIRouter(prefix="/api/v2/notifications")

  @router.post("", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
  async def create_notification(
      command: CreateNotificationCommand,
      usecase: CreateNotificationUseCase = Depends(get_create_notification_usecase),
  ):
      return await usecase.execute(command)

  @router.get("/{notification_id}", response_model=NotificationResponse)
  async def get_notification_by_id(
      notification_id: str,
      usecase: GetNotificationByIdUseCase = Depends(get_notification_by_id_usecase),
  ):
      query = GetNotificationByIdQuery(notification_id=notification_id)
      notification = await usecase.execute(query)
      if not notification:
          raise HTTPException(
              status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found"
          )
      return notification

  @router.get("", response_model=NotificationListResponse)
  async def list_notifications(
      notification_type: NotificationType | None = None,
      channel: NotificationChannel | None = None,
      user_id: str | None = None,
      status_filter: NotificationStatus | None = Query(default=None, alias="status"),
      is_important: bool | None = Query(default=None),
      attention_status: NotificationAttentionStatus | None = Query(default=None),
      limit: int = Query(10, ge=1, le=100),
      offset: int = Query(0, ge=0),
      usecase: ListNotificationsUseCase = Depends(get_list_notifications_usecase),
  ):
      query = ListNotificationsQuery(
          notification_type=notification_type,
          channel=channel,
          user_id=user_id,
          status=status_filter,
          is_important=is_important,
          attention_status=attention_status,
          limit=limit,
          offset=offset,
      )
      return await usecase.execute(query)
  ```
- **Highlighted** (optional): `true`
- **Explanation** (optional): Clean API design with query parameter filtering, pagination, and FastAPI dependency injection.

---

### Example 6 (`CodeExample`)

- **ID**: mongo-repository
- **Title**: MongoDB Repository Implementation
- **Description**: Async MongoDB repository using Motor driver with query builder pattern
- **Category**: infrastructure
- **Duration** (optional): 
- **Views** (optional): 
- **Tags** (optional):
  - mongodb
  - motor
  - repository
  - async

#### Files (`CodeFile[]`)

- **Name**: mongo_notification_repository.py
- **Path**: app/notification/infrastructure/repository/mongo_notification_repository.py
- **Language**: python
- **Content**:
  ```python
  from typing import Any, Dict, List, Optional

  from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

  from app.notification.application.queries.notification_queries import (
      ListNotificationsQuery,
  )
  from app.notification.domain.entities.models import Notification
  from app.notification.domain.enums import NotificationAttentionStatus, NotificationStatus
  from app.notification.domain.repository import NotificationRepository

  FILTER_MAPPING = {
      "notification_type": "notification_type",
      "channel": "channel",
      "user_id": "recipient.user_id",
      "status": "status",
      "is_important": "is_important",
      "attention_status": "attention_status",
      "source_event_type": "source_event_type",
  }


  class MongoNotificationRepository(NotificationRepository):
      def __init__(self, collection: AsyncIOMotorCollection) -> None:
          self._collection = collection

      async def get_by_id(self, notification_id: str) -> Optional[Notification]:
          doc = await self._collection.find_one({"_id": notification_id})
          if doc:
              return Notification.from_document(doc)
          return None

      async def get_by_event_id(self, event_id: str) -> Optional[Notification]:
          doc = await self._collection.find_one({"event_id": event_id})
          if doc:
              return Notification.from_document(doc)
          return None

      async def save(self, notification: Notification) -> Notification:
          doc = notification.to_document()
          await self._collection.insert_one(doc)
          return notification

      async def update(self, notification: Notification) -> Notification:
          doc = notification.to_document()
          await self._collection.replace_one(
              {"_id": notification.notification_id}, doc
          )
          return notification

      async def list_notifications(
          self, query: ListNotificationsQuery
      ) -> tuple[List[Notification], int]:
          filter_dict: Dict[str, Any] = {}
          for field, key in FILTER_MAPPING.items():
              value = getattr(query, field, None)
              if value is not None:
                  if isinstance(value, (NotificationStatus, NotificationAttentionStatus)):
                      filter_dict[key] = value.value
                  else:
                      filter_dict[key] = value

          total = await self._collection.count_documents(filter_dict)
          cursor = (
              self._collection.find(filter_dict)
              .sort("created_at", -1)
              .skip(query.offset)
              .limit(query.limit)
          )
          docs = await cursor.to_list(length=query.limit)
          notifications = [Notification.from_document(doc) for doc in docs]
          return notifications, total
  ```
- **Highlighted** (optional): `false`
- **Explanation** (optional): Async MongoDB operations with dynamic query building based on filter parameters.

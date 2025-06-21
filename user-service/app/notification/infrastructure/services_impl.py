from app.notification.application.services import NotificationService
from app.notification.domain.entitites import Notification
from app.queue.rabbitmq import rabbitmq_publisher

class NotificationServiceImpl(NotificationService):    
    async def send_notification(self, notification: Notification):
        await rabbitmq_publisher.connect()
        
        user = notification.user
        await rabbitmq_publisher.publish_token_request(
            user_email=user.email,
            token=notification.token,
            notification_type=notification.notification_type.value
        )
        
        await rabbitmq_publisher.close()
        
        
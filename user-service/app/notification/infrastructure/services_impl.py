from app.notification.application.services import NotificationService
from app.notification.domain.entitites import Notification
from config.app_config import Settings

#TODO: Inject
class NotificationServiceImpl(NotificationService):
    def __init__(self, settings: Settings) -> None:
        self.smtp_host = settings.rabbitmq_url
        super().__init__()
        
    
    async def send_notification(self, notification: Notification):
        pass
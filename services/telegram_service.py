from utils.api_clients.telegram_api_client import TelegramAPIClient
from utils.logger import get_logger

logger = get_logger(__name__)


class TelegramService:
    def __init__(self,
                 api_client: TelegramAPIClient,
                 chat_id):
        self.api_client = api_client
        self.chat_id = chat_id

    async def authenticate(self, token) -> None:
        await self.api_client.authenticate(token)

    async def user_reactivation_notification(self, notify_text=None, **kwargs):
        if not notify_text:
            notify_text = "The user is unblocked."

        await self.api_client.send_message(notify_text, chat_id=self.chat_id, **kwargs)

        logger.info(f"{notify_text}")

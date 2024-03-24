import os

import httpx

from utils.api_clients.base_api_client import BaseAPIClient

BOT_API_HOST = os.getenv("BOT_API_HOST")


class TelegramAPIClient(BaseAPIClient):

    def __init__(self, **kwargs):
        rate = 1 / 3  # Токены в секунду, 1/3 для 20 сообщений в минуту
        capacity = 20  # Максимальное количество токенов, 20 сообщений
        super().__init__(base_url=BOT_API_HOST, bucket_rate=rate, bucket_capacity=capacity, **kwargs)
        self.token = None

    async def authenticate(self, api_token=None) -> None:
        if api_token:
            self.token = api_token

    async def send_message(self, text, chat_id, no_preview=True, no_notification=True) -> httpx.Response:
        """
        https://telegram-bot-sdk.readme.io/reference/sendmessage
        """
        data = {"chat_id": chat_id,
                "text": text,
                "disable_web_page_preview": no_preview,
                "disable_notification": no_notification,
                "parse_mode": "HTML"}
        return await self.make_request("POST", "/sendMessage", data=data)

    async def make_request(self, method: str, endpoint: str, **kwargs) -> httpx.Response:
        endpoint = f"/bot{self.token}" + endpoint
        return await super().make_request(method, endpoint, **kwargs)

import os

import httpx

from datetime import timedelta

from utils.api_clients.base_api_client import BaseAPIClient

BOT_API_HOST = os.getenv("BOT_API_HOST")


class TelegramAPIClient(BaseAPIClient):

    def __init__(self, **kwargs):
        super().__init__(
            base_url=BOT_API_HOST,
            limiter_rate=20,
            limiter_period=timedelta(minutes=1),
            **kwargs)
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
        return await self._make_request("POST", "/sendMessage", data=data)

    async def _make_request(self, method: str, endpoint: str, **kwargs) -> httpx.Response:
        endpoint = f"/bot{self.token}" + endpoint
        return await super().make_request(method, endpoint, **kwargs)

import os
import httpx
import aiofiles

from datetime import datetime, time

from models.ticket import TicketData

from utils.api_clients.telegram_api_client import TelegramAPIClient
from utils.logger import get_logger

TEAM_CHAT_ID

class TelegramService:
    def __init__(self, api_client: TelegramAPIClient):
        self.api_client = api_client

    async def authenticate(self, token) -> None:
        await self.api_client.authenticate(token)

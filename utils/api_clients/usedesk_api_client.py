import os

import aiofiles

from datetime import timedelta
from pathlib import Path

from httpx import Response

from utils.api_clients.base_api_client import BaseAPIClient

USEDESK_API_HOST = os.getenv("USEDESK_API_HOST")


class UsedeskAPIClient(BaseAPIClient):

    def __init__(self, **kwargs):
        super().__init__(
            base_url=USEDESK_API_HOST,
            limiter_rate=5,
            limiter_period=timedelta(seconds=1),
            **kwargs)
        self.token = None

    async def authenticate(self, api_token=None) -> None:
        if api_token:
            self.token = api_token

    async def _make_request(self,
                            method: str,
                            endpoint: str,
                            file_paths: list[Path] | None = None,
                            **kwargs) -> Response:
        # Add an authentication token to the request body
        data = kwargs.get("data", {})
        data["api_token"] = self.token
        kwargs["data"] = data

        # Prepare files, if available
        files = await self.prepare_files(file_paths) if file_paths else None

        return await super().make_request(method, endpoint, files=files, **kwargs)

    @staticmethod
    async def prepare_files(file_paths: list[Path] | None) -> list[tuple[str, tuple[str, bytes]]] | None:
        prepared_files = []

        for file_path in file_paths:
            async with aiofiles.open(file_path, 'rb') as f:
                file_name = file_path.name
                file_content = await f.read()
                prepared_files.append(('files[]', (file_name, file_content)))

        return prepared_files if prepared_files else None

    async def send_message(self,
                           message,
                           ticket_id,
                           agent_id,
                           file_paths: list[Path] | None = None):
        """
        https://api.usedocs.ru/article/33740
        """
        data = {
            "ticket_id": ticket_id,
            "message": message,
            "type": "public",
            "user_id": agent_id,
            "from": "user",
        }
        return await self._make_request("POST", "/create/comment", data=data, file_paths=file_paths)

    async def update_ticket(self,
                            ticket_id,
                            category_lid,
                            field_id=19402,
                            status=2) -> Response:
        """
        https://api.usedocs.ru/article/33737

        Status list: https://api.usedocs.ru/article/33728
        """
        data = {
            "ticket_id": ticket_id,
            "field_id": field_id,
            "field_value": category_lid,
            "status": status,
        }
        return await self._make_request("POST", "/update/ticket", data=data)

import os
from httpx import Response

from utils.api_clients.base_api_client import BaseAPIClient

USEDESK_API_HOST = os.getenv("USEDESK_API_HOST")


class UsedeskAPIClient(BaseAPIClient):

    def __init__(self, **kwargs):
        super().__init__(base_url=USEDESK_API_HOST, **kwargs)
        self.token = None

    async def authenticate(self, api_token=None) -> None:
        if api_token:
            self.token = api_token

    async def make_request(self, method: str, endpoint: str, files=None, **kwargs) -> Response:
        # Add an authentication token to the request body
        data = kwargs.get("data", {})
        data["api_token"] = self.token
        kwargs["data"] = data

        # Prepare files, if available
        prepared_files = []
        if files:
            for file_path, file_content in files:
                file_name = file_path.split("/")[-1]
                prepared_files.append(('files[]', (file_name, file_content)))

        return await super().make_request(method, endpoint, files=prepared_files, **kwargs)

    async def send_message(self,
                           message,
                           ticket_id,
                           agent_id,
                           files: list[tuple[str, bytes] | None] = None):
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
        return await self.make_request("POST", "/create/comment", data=data, files=files)

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
        return await self.make_request("POST", "/update/ticket", data=data)

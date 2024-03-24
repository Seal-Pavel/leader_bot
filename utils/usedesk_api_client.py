import os
import httpx

from utils.base_api_client import BaseAPIClient

USEDESK_API_HOST = os.getenv("USEDESK_API_HOST")
USEDESK_API_TOKEN = os.getenv('USEDESK_API_TOKEN')


class UsedeskAPIClient(BaseAPIClient):

    def __init__(self, **kwargs):
        super().__init__(base_url=USEDESK_API_HOST, **kwargs)
        self.token: str = USEDESK_API_TOKEN

    async def authenticate(self, api_token=None) -> None:
        self.token = api_token if api_token else USEDESK_API_TOKEN

    async def make_request(self, method: str, endpoint: str, **kwargs) -> httpx.Response:
        data = kwargs.get("data", {})
        data["api_token"] = self.token
        kwargs["data"] = data

        if "files" in kwargs and kwargs["files"] is not None:
            kwargs["files"] = [('files[]', open(f, "rb")) for f in kwargs["files"]]

        response = await super().make_request(method, endpoint, **kwargs)

        return response

    async def send_message(self, message, ticket_id, fls: list[str] = None, agent_id=None) -> httpx.Response:
        """
        https://api.usedocs.ru/article/33740
        """
        if not agent_id:
            agent_id = 247423

        payload = {
            "ticket_id": ticket_id,
            "message": message,
            "type": "public",
            "user_id": agent_id,
            "from": "user",
        }
        b_files = [('files[]', open(f, "rb")) for f in fls] if fls else None
        response = await self.make_request("POST", "/create/comment", data=payload, files=b_files)
        if b_files:
            for _, f in b_files:
                f.close()

        return response

    async def update_ticket(self, ticket_id, category_lid, field_id=None, status=2) -> httpx.Response:
        """
        https://api.usedocs.ru/article/33737
        """
        if not field_id:
            field_id = 19402

        payload = {
            "ticket_id": ticket_id,
            "field_id": field_id,
            "field_value": category_lid,
            "status": status,
        }
        response = await self.make_request("POST", "/update/ticket", data=payload)

        return response

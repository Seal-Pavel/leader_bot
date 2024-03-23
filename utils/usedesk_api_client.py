import os
import httpx

from utils.base_api_client import BaseAPIClient

USEDESK_API_HOST = os.getenv("USEDESK_API_HOST")
USEDESK_API_UPDATE_TICKET = "update/ticket"
USEDESK_API_GET_FIELDS = "ticket/fields"

USEDESK_API_TOKEN = os.getenv('USEDESK_API_TOKEN')


class UsedeskAPIClient(BaseAPIClient):

    def __init__(self, **kwargs):
        super().__init__(base_url=USEDESK_API_HOST, **kwargs)
        self.token: str = USEDESK_API_TOKEN

    async def authenticate(self, email=None, password=None) -> None:
        pass

    async def send_message(self, message, ticket, fls: list[str] = None, agent_id=247423) -> httpx.Response:
        payload = {
            "api_token": USEDESK_API_TOKEN,
            "ticket_id": ticket,
            "message": message,
            "type": "public",
            "user_id": agent_id,
            "from": "user",
        }
        b_files = [('files[]', open(f, "rb")) for f in fls] if fls else None
        response = self.make_request("POST", "create/comment", data=payload, files=b_files)
        if b_files:
            for _, f in b_files:
                f.close()
        return response

    # async def update_ticket(ticket, category_lid, field_id=19402, status=2) -> httpx.Response:
    #     payload = {
    #         "api_token": api_token,
    #         "ticket_id": ticket,
    #         "field_id": field_id,
    #         "field_value": category_lid,
    #         "status": status,
    #     }
    #     return requests.post(update_ticket_url, data=payload)

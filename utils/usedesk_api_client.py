import os

from utils.base_api_client import BaseAPIClient

USEDESK_API_HOST = os.getenv("USEDESK_API_HOST")


class UsedeskAPIClient(BaseAPIClient):

    def __init__(self, **kwargs):
        super().__init__(base_url=USEDESK_API_HOST, **kwargs)

    async def authenticate(self, email=None, password=None) -> None:
        pass

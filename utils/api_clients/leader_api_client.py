import os
import httpx

from urllib.parse import urlencode
from utils.api_clients.base_api_client import BaseAPIClient

LEADER_ID_API_HOST = os.getenv("LEADER_ID_API_HOST")


class LeaderAPIClient(BaseAPIClient):
    def __init__(self, **kwargs):
        super().__init__(base_url=LEADER_ID_API_HOST, **kwargs)

    async def update_token(self, token: str) -> None:
        self.client.headers.update({"Authorization": f"Bearer {token}"})

    async def authenticate(self, email, password) -> None:
        url = "/auth/login"
        data = {"email": email, "password": password}
        response = await self._make_request(
            "POST",
            url,
            should_retry=False,
            allow_reauth=False,
            json=data)
        token = response.json()["data"]["access_token"]
        self.client.headers.update({"Authorization": f"Bearer {token}"})

    async def _make_request(self, method: str, endpoint: str, allow_reauth=True, **kwargs) -> httpx.Response:
        try:
            return await super().make_request(method, endpoint, **kwargs)

        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 401 and allow_reauth:
                await self.authenticate()
                return await super().make_request(method, endpoint, **kwargs)
            if exc.response.status_code == 422:
                raise CaptchaNotSetException(server_response=exc.response.text)
            raise

    async def _search_users(self, query: str | int, count=1) -> list:
        params = {"query": str(query).lower(),
                  "paginationSize": count,
                  "paginationPage": 1}
        full_url = f"/admin/users?{urlencode(params)}"
        response = await self._make_request(
            "GET",
            full_url)
        users_data: list = response.json()['data']['_items']

        if not users_data:
            raise UserNotFoundException(query)
        return users_data

    async def get_user(self, user: str | int) -> dict:
        if isinstance(user, str):
            user_data = await self._search_users(user)
            user_id = user_data[0]['id']
        else:
            user_id = user

        url = f"/users/{user_id}"
        response = await self._make_request(
            "GET",
            url)
        return response.json()

    async def _perform_user_action(self, user_id: int, action_path: str, check_existence: bool = False) -> dict:
        if check_existence:
            await self._search_users(user_id)

        data = {"userId": user_id}
        url = action_path
        response = await self._make_request(
            "POST",
            url,
            json=data)
        return response.json()

    async def unlocking_user(self, user: int, check_existence=False) -> dict:
        return await self._perform_user_action(user, "/admin/users/refresh-verification-profile", check_existence)

    async def approve_user(self, user: int, check_existence=False) -> dict:
        return await self._perform_user_action(user, "/admin/users/approve-profile", check_existence)


class UserNotFoundException(Exception):
    def __init__(self, user):
        self.user_query = user
        super().__init__(f"404 User with query '{user}' not found.")


class CaptchaNotSetException(Exception):
    def __init__(self, server_response="Captcha is required"):
        self.message = server_response
        super().__init__(self.message)

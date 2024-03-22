from models.user import User

from utils.leader_api_client import LeaderAPIClient


class LeaderServices:
    def __init__(self, api_client: LeaderAPIClient):
        self.api_client = api_client
        self.user_service: UserService | None = None
        self.event_service: EventService | None = None

    async def authenticate(self, email=None, password=None) -> None:
        await self.api_client.authenticate(email, password)
        self.user_service = UserService(self.api_client)
        self.event_service = EventService(self.api_client)

    async def update_token(self, token: str) -> None:
        await self.api_client.update_token(token)


class UserService:
    def __init__(self, api_client: LeaderAPIClient):
        self.api_client = api_client
        self.user: User | None = None

    async def load_user(self, user: str | int):
        user_json_data = await self.api_client.get_user(user)
        self.user = User.model_validate(user_json_data)

    async def is_user_blocked(self) -> bool:
        if self.user is None:
            raise ValueError("User not loaded. Please call load_user first.")
        return self.user.status in [8, 9]

    async def unlocking_and_approve(self) -> None:
        await self.api_client.unlocking_user(self.user.id)
        await self.api_client.approve_user(self.user.id)


class EventService:
    def __init__(self, api_client: LeaderAPIClient):
        self.api_client = api_client

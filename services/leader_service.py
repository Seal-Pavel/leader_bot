from models.user import User

from utils.api_clients.leader_api_client import LeaderAPIClient
from utils.logger import get_logger

logger = get_logger(__name__)


class LeaderServices:
    def __init__(self, api_client: LeaderAPIClient):
        self.api_client = api_client
        self.user_service: UserService | None = None
        self.event_service: EventService | None = None

    async def authenticate(self, email, password) -> None:
        await self.api_client.authenticate(email, password)
        self.user_service = UserService(self.api_client)
        self.event_service = EventService(self.api_client)

    async def update_token(self, token: str) -> None:
        await self.api_client.update_token(token)


class UserService:
    def __init__(self, api_client: LeaderAPIClient):
        self.api_client = api_client
        self.user: User | None = None

    async def reactivate(self, user: str | int) -> tuple[bool, str]:
        await self.load_user(user)

        if await self.is_user_blocked() or self.user.id == 1127536:
            await self.unlocking_and_approve()
            logger.info(f'User with ID {self.user.id} and date of birth {self.user.birthday} has been unblocked.')
            return True, "User reactivated successfully."
        else:
            return False, "User activation is not required."

    async def load_user(self, user: str | int):
        user_json_data = await self.api_client.get_user(user)
        self.user = User.model_validate(user_json_data)

    async def is_user_blocked(self) -> bool:
        if self.user is None:
            raise ValueError("User not loaded. Please call load_user first.")
        return self.user.status in [8, 9]

    async def unlocking_and_approve(self) -> None:
        if self.user is None:
            raise ValueError("User not loaded. Please call load_user first.")
        await self.api_client.unlocking_user(self.user.id)
        await self.api_client.approve_user(self.user.id)


class EventService:
    def __init__(self, api_client: LeaderAPIClient):
        self.api_client = api_client

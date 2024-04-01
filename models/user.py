from pydantic import BaseModel, Extra
from datetime import datetime


class UserData(BaseModel):
    id: int
    email: str
    name: str | None
    status: int | None
    birthday: datetime | None
    emailConfirmed: bool | None
    agreement: bool | None
    lastSeen: datetime | None
    createdAt: datetime | None

    class Config:
        extra = Extra.allow


class User(BaseModel):
    data: UserData

    class Config:
        extra = Extra.allow

from pydantic import BaseModel, Extra
from datetime import datetime


class UserData(BaseModel):
    id: int
    email: str
    name: str
    status: int
    birthday: datetime
    emailConfirmed: bool
    agreement: bool
    lastSeen: datetime
    createdAt: datetime

    class Config:
        extra = Extra.allow


class User(BaseModel):
    data: UserData

    class Config:
        extra = Extra.allow

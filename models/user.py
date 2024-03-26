from pydantic import BaseModel, Extra
from datetime import datetime


class UserData(BaseModel):
    id: int
    email: str | None
    last_name: str
    first_name: str
    father_name: str | None
    status: int
    gender: str
    birthday: datetime
    email_confirmed: bool
    personal_data_agreement: bool
    agreement: bool
    last_seen: datetime
    age: int
    registrationAt: datetime

    class Config:
        extra = Extra.allow


class User(BaseModel):
    data: UserData

    class Config:
        extra = Extra.allow

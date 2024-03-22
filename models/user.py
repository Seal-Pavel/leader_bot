from pydantic import BaseModel, Extra
from datetime import datetime


class User(BaseModel):
    id: int
    birthday: datetime | None
    name: str
    email: str
    phone: str | None
    telegram: str | None
    phoneConfirmed: bool
    emailConfirmed: bool
    phones: list | None
    role: str
    roleName: str
    createdAt: datetime
    status: int
    lastSeen: datetime
    registrationType: str
    createdByApi: str | None
    uploadedDocuments: dict | None

    class Config:
        extra = Extra.allow

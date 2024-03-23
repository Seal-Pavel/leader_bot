from pydantic import BaseModel


class TicketData(BaseModel):
    id: str
    subject: str
    client_email: str
    status: str


class TicketRequest(BaseModel):
    url: str
    data: TicketData
    headers: list[str]

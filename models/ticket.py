from pydantic import BaseModel


class TicketData(BaseModel):
    client_email: str
    ticket_subject: str
    ticket_id: str
    ticket_status: str


class TicketRequest(BaseModel):
    url: str
    data: TicketData
    headers: list[str]

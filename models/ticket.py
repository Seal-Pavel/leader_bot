from pydantic import BaseModel


class TicketRequest(BaseModel):
    id: str
    subject: str
    client_email: str
    status: str

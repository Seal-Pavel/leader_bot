from pydantic import BaseModel
from datetime import time


class Schedule(BaseModel):
    weekdays: list[int]  # (0 = Monday)
    start_time: time
    end_time: time


class Agent(BaseModel):
    usedesk_id: int
    name: str | None
    schedule: list[Schedule]

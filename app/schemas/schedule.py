from datetime import date, datetime
from typing import Literal, Optional

from pydantic import BaseModel


# ---------------CREATED SCHEDULE SCHEMA----------#
class ScheduleBase(BaseModel):
    subscription_id: int
    task_name: str
    status: Optional[Literal["pending", "complete", "cancelled"]] = "pending"


class ScheduleCreate(ScheduleBase):
    pass


class ScheduleUpdate(BaseModel):
    status: Literal["pending", "complete", "cancelled"] = None


class ScheduleOut(ScheduleBase):
    schedule_id: int
    schedule_date: date
    created_at: datetime

    class Config:
        orm_mode = True

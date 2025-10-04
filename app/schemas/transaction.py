# flake8: noqa: F401
from datetime import datetime

from pydantic import BaseModel


class TransactionBase(BaseModel):
    subscription_id: int


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    subscription_id: int | None = None


class TransactionOut(TransactionBase):
    transaction_id: int
    created_at: datetime

    class Config:
        orm_mode = True

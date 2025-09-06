from pydantic import BaseModel
from datetime import datetime

#---------------CREATED TRANSACTION SCHEMA----------#

class TransactionBase(BaseModel):
    subscription_id: int


class TransactionCreate(TransactionBase):
    pass



class TransactionOut(TransactionBase):
    transaction_id: int
    created_at: datetime

    class Config:
        orm_mode = True
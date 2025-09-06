from pydantic import BaseModel
from datetime import datetime
from typing import Optional


#---------------CREATED TRANSACTION FAILURE SCHEMA----------#

class Transaction_Failure_Base(BaseModel):
    transaction_id: int
    failure_reason: Optional[str]


class Transaction_Failure_Out(Transaction_Failure_Base):
    transaction_failure_id: int
    failed_at: datetime

    class Config:
        orm_mode = True
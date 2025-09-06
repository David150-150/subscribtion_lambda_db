from pydantic import BaseModel
from typing import Optional, Literal

#---------------CREATED TRANSACTION DETAIL SCHEMA----------#
class Transaction_Detail_Base(BaseModel):
    transaction_id: int
    action_task: Optional[str]
    status: Optional[Literal["successful", "unsuccessful", ""]] = "successful"
    message: Optional[str]


class Transaction_Detail_Out(Transaction_Detail_Base):
    transaction_details_id: int

    class Config:
        orm_mode = True

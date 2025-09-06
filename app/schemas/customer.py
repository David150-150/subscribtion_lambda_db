
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

#---------------CREATED CUSTOMER SCHEMA----------#

class CustomerBase(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    email: EmailStr
    telephone: str
    #password: str


class CustomerCreate(CustomerBase):
    password: str


class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    telephone: Optional[str] = None
    password: Optional[str] = None


class CustomerOut(CustomerBase):
    customer_id: int
    created_at: datetime

    class Config:
        orm_mode = True

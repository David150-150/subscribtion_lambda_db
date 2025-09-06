
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

#---------------CREATED PRODUCT SCHEMA----------#

class ProductBase(BaseModel):
    name: str
    description: str
    price: float


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None





class ProductOut(ProductBase):
    product_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal

#---------------CREATED SUBSCRIPTION SCHEMA----------#
class SubscriptionBase(BaseModel):
    status: Optional[Literal["active", "inactive", "cancelled"]] = Field(default = "active",
            description = "The current status of your subscription"                   )
    customer_id: int
    product_id: int
    

class SubscriptionCreate(SubscriptionBase):
    pass


class SubscriptionUpdate(BaseModel):
    status: Optional[Literal["active", "inactive", "cancelled"]] = None



class SubscriptionOut(SubscriptionBase):
    subscription_id: int
    subscribed_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
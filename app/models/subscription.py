from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.sql import func
from app.db import Base



#---------------CREATE SUBSCRIPTION TABLE-------------#
class Subscription(Base):
    __tablename__ = "subscription"

    subscription_id = Column(Integer, primary_key = True, index = True, autoincrement = True)
    customer_id = Column(Integer, ForeignKey("customer.customer_id"), nullable = False)
    product_id = Column(Integer, ForeignKey("product.product_id"), nullable = False)
    status = Column(Enum("active", "inactive", "cancelled", name = "subscription_status_enum"), nullable = False, default = "active")
    subscribed_at = Column(TIMESTAMP, server_default = func.now())
    updated_at = Column(TIMESTAMP, server_default = func.now(), onupdate = func.now())
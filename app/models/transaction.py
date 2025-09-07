from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer
from sqlalchemy.sql import func

from app.db import Base


# -------------------CREATE TRANSACTION-----------#
class Transaction(Base):
    __tablename__ = "transaction"

    transaction_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    subscription_id = Column(
        Integer, ForeignKey("subscription.subscription_id"), nullable=False
    )
    created_at = Column(TIMESTAMP, server_default=func.now())

# flake8: noqa: F401
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db import Base


class Transaction(Base):
    __tablename__ = "transaction"

    transaction_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    subscription_id = Column(Integer, ForeignKey("subscription.subscription_id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    details = relationship("TransactionDetails", backref="transaction", cascade="all, delete-orphan", passive_deletes=True)

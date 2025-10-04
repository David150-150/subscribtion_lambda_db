# flake8: noqa: F401
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.db import Base

# # -------------CREATE TRANSACTION FAILURE TABLE--------------#


class TransactionFailures(Base):
    __tablename__ = "transaction_failures"

    transaction_failure_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    transaction_id = Column(Integer, ForeignKey("transaction.transaction_id", ondelete="CASCADE"), nullable=False)  # <-- Important!
    failure_reason = Column(String(50), nullable=False)
    failed_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

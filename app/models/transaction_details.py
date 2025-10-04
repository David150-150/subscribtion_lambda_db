# flake8: noqa: F401
from sqlalchemy import TIMESTAMP, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.db import Base


class TransactionDetails(Base):
    __tablename__ = "transaction_details"

    transaction_details_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    transaction_id = Column(
        Integer,
        ForeignKey("transaction.transaction_id", ondelete="CASCADE"),
        nullable=False,
    )
    action_task = Column(String(30), nullable=False)
    message = Column(String(30), nullable=False)
    status = Column(
        Enum("successful", "unsuccessful", name="transaction_status"),
        nullable=False,
        server_default="successful",
    )

from sqlalchemy import Column, Enum, ForeignKey, Integer, String

from app.db import Base


# --------------TRANSACTION DETAILS TABLE---------------#
class TransactionDetails(Base):
    __tablename__ = "transaction_details"

    transaction_details_id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(
        Integer, ForeignKey("transaction.transaction_id"), nullable=False
    )
    action_task = Column(String(30), nullable=False)
    message = Column(String(30), nullable=False)
    status = Column(
        Enum("successful", "unsuccessful", name="transaction_status"),
        nullable=False,
        default="successful",
    )

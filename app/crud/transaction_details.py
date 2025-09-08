# flake8: noqa: F401

from typing import Optional

from sqlalchemy.orm import Session

from app.models import TransactionDetails
from app.schemas.transaction_details import Transaction_Detail_Base


# -----------------CREATE TRANSACTION DETAIL------------#
def transaction_detail_create(db: Session, transaction_details: Transaction_Detail_Base) -> TransactionDetails:
    new_transaction_detail = TransactionDetails(**transaction_details.dict())
    db.add(new_transaction_detail)
    db.commit()
    db.refresh(new_transaction_detail)
    return new_transaction_detail


# -----------------GET ALL TRANSACTION DETAIL------------#
def read_transaction_details(db: Session):
    return db.query(TransactionDetails).all()


# -----------------GET TRANSACTION DETAIL------------#
def read_transaction_detail(db: Session, transaction_details_id: int) -> Optional[TransactionDetails]:
    return db.query(TransactionDetails).filter(TransactionDetails.transaction_details_id == transaction_details_id).first()

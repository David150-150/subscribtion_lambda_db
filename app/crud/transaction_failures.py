from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import TransactionFailures
from app.schemas.transaction_failures import Transaction_Failure_Base


# -----------------CREATE TRANSACTION FAILURE------------#
def create_transaction_failure(db: Session, transaction_failure: Transaction_Failure_Base) -> TransactionFailures:
    new_transaction_failure = TransactionFailures(**transaction_failure.dict())
    db.add(new_transaction_failure)
    db.commit()
    db.refresh(new_transaction_failure)
    return new_transaction_failure


# -----------------GET ALL TRANSACTION FAILURE------------#
def read_transaction_failures(db: Session) -> List[TransactionFailures]:
    return db.query(TransactionFailures).all()


# -----------------GET TRANSACTION FAILURE------------#
def read_transaction_failure(db: Session, transaction_failure_id: int) -> Optional[TransactionFailures]:
    return db.query(TransactionFailures).filter(TransactionFailures.transaction_failure_id == transaction_failure_id).first()

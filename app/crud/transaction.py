# flake8: noqa: F401
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate


# -----------------CREATE TRANSACTION------------#
def create_transaction(db: Session, transaction: TransactionCreate) -> Transaction:
    new_transaction = Transaction(**transaction.dict())
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction


# -----------------GET ALL TRANSACTIONS------------#
def get_transactions(db: Session) -> List[Transaction]:
    return db.query(Transaction).all()


# -----------------GET SINGLE TRANSACTION------------#
def get_transaction(db: Session, transaction_id: int) -> Optional[Transaction]:
    return db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()


# -----------------UPDATE TRANSACTION------------#
def update_transaction(db: Session, transaction_id: int, transaction_data: TransactionUpdate) -> Optional[Transaction]:
    transaction = get_transaction(db, transaction_id)
    if not transaction:
        return None

    for key, value in transaction_data.dict(exclude_unset=True).items():
        setattr(transaction, key, value)

    db.commit()
    db.refresh(transaction)
    return transaction


# -----------------DELETE TRANSACTION------------#
def delete_transaction(db: Session, transaction_id: int) -> Optional[Transaction]:
    transaction = get_transaction(db, transaction_id)
    if not transaction:
        return None
    db.delete(transaction)
    db.commit()
    return transaction

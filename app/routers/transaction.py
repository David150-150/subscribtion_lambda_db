# flake8: noqa: F401
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import get_db

router = APIRouter()


@router.post("/", response_model=schemas.TransactionOut, status_code=201)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    return crud.transaction.create_transaction(db, transaction)


@router.get("/", response_model=List[schemas.TransactionOut])
def read_transactions(db: Session = Depends(get_db)):
    return crud.transaction.get_transactions(db)


@router.get("/{transaction_id}", response_model=schemas.TransactionOut)
def read_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = crud.transaction.get_transaction(db, transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=404,
            detail=f"The transaction ID:{transaction_id} does not exist",
        )
    return transaction


@router.put("/{transaction_id}", response_model=schemas.TransactionOut)
def update_transaction(transaction_id: int, transaction_data: schemas.TransactionCreate, db: Session = Depends(get_db)):
    update = crud.transaction.update_transaction(db, transaction_id, transaction_data)
    if not update:
        raise HTTPException(
            status_code=404,
            detail=f"The transaction ID:{transaction_id} does not exist",
        )
    return update


@router.delete("/{transaction_id}", status_code=200)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    delete = crud.transaction.delete_transaction(db, transaction_id)
    if not delete:
        raise HTTPException(
            status_code=404,
            detail=f"The transaction ID:{transaction_id} does not exist",
        )
    return {"message": f"Transaction with ID {transaction_id} deleted successfully"}

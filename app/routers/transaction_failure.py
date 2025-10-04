# flake8: noqa: F401
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import get_db

router = APIRouter()


# --------------CREATED ALL TRANSACTION FAILURE ROUTES-------------#
@router.post("/", response_model=schemas.Transaction_Failure_Out)
def create_transaction_failure(
    transaction_failures: schemas.Transaction_Failure_Base,
    db: Session = Depends(get_db),
):
    return crud.transaction_failures.create_transaction_failure(db, transaction_failures)


@router.get("/", response_model=List[schemas.Transaction_Failure_Out])
def get_transaction_failures(db: Session = Depends(get_db)):
    return crud.transaction_failures.read_transaction_failures(db)


@router.get("/{transaction_failure_id}", response_model=schemas.Transaction_Failure_Out)
def get_transaction_failure(transaction_failure_id: int, db: Session = Depends(get_db)):
    transaction_failure = crud.transaction_failures.read_transaction_failure(db, transaction_failure_id)
    if not transaction_failure:
        raise HTTPException(status_code=404, detail=f"ID:{transaction_failure_id}, not found")
    return transaction_failure

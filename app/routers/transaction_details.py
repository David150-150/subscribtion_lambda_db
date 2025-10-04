# flake8: noqa: F401
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import get_db

router = APIRouter()


# --------------CREATED ALL TRANSACTION DETAIL ROUTES-------------#
@router.post("/", response_model=schemas.Transaction_Detail_Out, status_code=201)
def create_transaction_details(transaction_details: schemas.Transaction_Detail_Base, db: Session = Depends(get_db)):
    return crud.transaction_details.transaction_detail_create(db, transaction_details)


@router.get("/", response_model=List[schemas.Transaction_Detail_Out])
def get_transaction_details(db: Session = Depends(get_db)):
    return crud.transaction_details.read_transaction_details(db)


@router.get("/{transaction_detail_id}", response_model=schemas.Transaction_Detail_Out)
def get_transaction_detail(transaction_detail_id: int, db: Session = Depends(get_db)):
    transaction_detail = crud.transaction_details.read_transaction_detail(db, transaction_detail_id)
    if not transaction_detail:
        raise HTTPException(status_code=404, detail=f"ID:{transaction_detail_id}, not found")
    return transaction_detail

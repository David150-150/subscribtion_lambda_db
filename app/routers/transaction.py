from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.db import get_db
from app import schemas, crud
from typing import List

router = APIRouter()

#--------------CREATED ALL TRANSACTION ROUTES-------------#
@router.post("/", response_model = schemas.TransactionOut)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    return crud.transaction.create_transaction(db, transaction)


@router.get("/", response_model = List[schemas.TransactionOut])
def read_transactions(db: Session = Depends(get_db)):
    return crud.transaction.get_transactions(db)


@router.get("/{transaction_id}", response_model = schemas.TransactionOut)
def read_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = crud.transaction.get_transaction(db, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail=f"The transaction ID:{transaction_id}, does not exit")
    return transaction



# @router.put("/{transaction_id}", response_model = Depends(get_db))
# def update_transaction(transacton_id: int, transaction_data: schemas.TransactionOut, db: Session = Depends(get_db)):
#     update = crud.transaction.update_transaction(db, transacton_id, transaction_data)
#     if not update:
#         raise HttpException(status_code = 404, details = "The transaction ID:{transaction_id}, does not exit")
#     return update


# @router.delete("/{transaction_id}")
# def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
#     delete = crud.transaction.delete_transaction(db, transaction_id)
#     if not delete:
#         raise HttpException(status_code = 404, details = "The transaction ID:{transaction_id}, does not exit")
#     return delete

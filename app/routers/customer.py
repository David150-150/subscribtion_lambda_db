# app/routers/customer.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import get_db

# ----------------CREATED ALL CUSTOMER ROUTES-------------#
router = APIRouter()


@router.get("/", response_model=List[schemas.CustomerOut])
def read_customers(db: Session = Depends(get_db)):
    return crud.customer.get_customers(db)


@router.get("/{customer_id}", response_model=schemas.CustomerOut)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = crud.customer.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.put("/{customer_id}", response_model=schemas.CustomerOut)
def update_customer(
    customer_id: int,
    customer_data: schemas.CustomerUpdate,
    db: Session = Depends(get_db),
):
    updated_customer = crud.customer.update_customer(db, customer_id, customer_data)
    if not updated_customer:
        raise HTTPException(status_code=404, detail="Updated customer not found")
    return updated_customer


@router.delete("/{customer_id}", status_code=200)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = crud.customer.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    crud.customer.delete_customer(db, customer_id)
    return {"message": "Customer successfully deleted"}

# flake8: noqa: F401
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import get_db

router = APIRouter()


@router.post("/", response_model=schemas.CustomerOut, status_code=201)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    db_customer = crud.customer.get_customer_by_email(db, customer.email)
    if db_customer:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.customer.create_customer(db, customer)


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
def update_customer(customer_id: int, customer_data: schemas.CustomerUpdate, db: Session = Depends(get_db)):
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

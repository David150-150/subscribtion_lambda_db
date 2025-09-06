# app/crud/customer.py
from sqlalchemy.orm import Session
from app import models, schemas
from app.models import Customer
from typing import List, Optional

# -------------------- Create Customer -------------------- #
def create_customer(db: Session, customer: schemas.CustomerCreate) -> Customer:
    new_customer = models.Customer(**customer.dict())  # Assume password is already hashed
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

# -------------------- Get All Customers -------------------- #
def get_customers(db: Session, skip: int = 0, limit: int = 10) -> List[Customer]:
    return db.query(Customer).offset(skip).limit(limit).all()

# -------------------- Get Single Customer -------------------- #
def get_customer(db: Session, customer_id: int) -> Optional[Customer]:
    return db.query(Customer).filter(Customer.customer_id == customer_id).first()

# -------------------- Update Customer -------------------- #
def update_customer(db: Session, customer_id: int, customer_data: schemas.CustomerUpdate) -> Optional[Customer]:
    customer = get_customer(db, customer_id)
    if not customer:
        return None
    for key, value in customer_data.dict(exclude_unset=True).items():
        setattr(customer, key, value)
    db.commit()
    db.refresh(customer)
    return customer

# -------------------- Delete Customer -------------------- #
def delete_customer(db: Session, customer_id: int) -> Optional[Customer]:
    customer = get_customer(db, customer_id)
    if customer:
        db.delete(customer)
        db.commit()
        return customer
    return None

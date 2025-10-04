# flake8: noqa: F401
# app/crud/customer.py
from typing import List, Optional

from sqlalchemy.orm import Session

from app import models, schemas
from app.models import Customer
from app.utils import hash_password


def create_customer(db: Session, customer: schemas.CustomerCreate) -> Customer:
    """
    Creates a new customer with a hashed password.
    """
    hashed = hash_password(customer.password)
    new_customer = models.Customer(
        first_name=customer.first_name,
        middle_name=customer.middle_name,
        last_name=customer.last_name,
        email=customer.email,
        telephone=customer.telephone,
        hashed_password=hashed,
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer


def get_customers(db: Session, skip: int = 0, limit: int = 10) -> List[Customer]:
    return db.query(Customer).offset(skip).limit(limit).all()


def get_customer(db: Session, customer_id: int) -> Optional[Customer]:
    return db.query(Customer).filter(Customer.customer_id == customer_id).first()


def get_customer_by_email(db: Session, email: str) -> Optional[Customer]:
    return db.query(Customer).filter(Customer.email == email).first()


def update_customer(db: Session, customer_id: int, customer_data: schemas.CustomerUpdate) -> Optional[Customer]:
    customer = get_customer(db, customer_id)
    if not customer:
        return None

    update_data = customer_data.dict(exclude_unset=True)

    # If password is provided, hash it before updating
    if "password" in update_data:
        update_data["hashed_password"] = hash_password(update_data.pop("password"))

    for key, value in update_data.items():
        setattr(customer, key, value)

    db.commit()
    db.refresh(customer)
    return customer


def delete_customer(db: Session, customer_id: int) -> Optional[Customer]:
    customer = get_customer(db, customer_id)
    if customer:
        db.delete(customer)
        db.commit()
        return customer
    return None

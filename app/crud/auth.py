# flake8: noqa: F401
from fastapi import HTTPException  # <-- import at the top
from sqlalchemy.orm import Session

from app.models import Customer
from app.schemas import CustomerCreate
from app.utils.password import hash_password, verify_password


def register_customer(db: Session, customer: CustomerCreate):
    # Check if email already exists
    existing = db.query(Customer).filter(Customer.email == customer.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    hashed = hash_password(customer.password)
    new_customer = Customer(first_name=customer.first_name, middle_name=customer.middle_name, last_name=customer.last_name, email=customer.email, telephone=customer.telephone, hashed_password=hashed)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(Customer).filter(Customer.email == email).first()
    if user and verify_password(password, user.hashed_password):
        return user
    return None

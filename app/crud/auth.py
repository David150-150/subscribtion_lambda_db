# app/crud/auth.py
from typing import Optional

from sqlalchemy.orm import Session

from app import models, schemas
from app.models import Customer

# from app.utils import hash_password, verify_password
from app.utils.password import hash_password, verify_password


def register_customer(db: Session, customer: schemas.CustomerCreate) -> Customer:
    customer_data = customer.dict()

    # Extract plain password, hash it, and remove the original
    plain_password = customer_data.pop("password")
    customer_data["hashed_password"] = hash_password(plain_password)

    new_customer = models.Customer(**customer_data)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer


def authenticate_user(db: Session, email: str, password: str) -> Optional[Customer]:
    user = db.query(Customer).filter(Customer.email == email).first()
    if user and verify_password(password, user.hashed_password):
        return user
    return None

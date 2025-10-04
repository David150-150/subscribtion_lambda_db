# flake8: noqa: F401
from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.auth.auth_handler import create_access_token
from app.crud import auth as auth_crud
from app.db import get_db

router = APIRouter()


@router.post("/signup", response_model=schemas.CustomerOut, status_code=201)
def signup(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return auth_crud.register_customer(db, customer)


@router.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = auth_crud.authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

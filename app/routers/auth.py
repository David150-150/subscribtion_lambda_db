# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app import schemas
from app.db import get_db
from app.auth.auth_handler import create_access_token
from app.crud import auth as auth_crud  # Use separate auth crud
from app.utils.password import hash_password


router = APIRouter(prefix="/auth", tags=["Authentication"])

# ------------------ Sign Up ------------------ #
@router.post("/signup", response_model=schemas.CustomerOut)
def signup(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return auth_crud.register_customer(db, customer)

# # ------------------ Login ------------------ #
@router.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = auth_crud.authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


# flake8: noqa: F401
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import get_db

router = APIRouter()


# ----------------------CREATED ALL PRODUCT ROUTES-----------------#
@router.post("/", response_model=schemas.ProductOut)
def create(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.product.create_product(db, product)


@router.get("/", response_model=List[schemas.ProductOut])
def read_products(db: Session = Depends(get_db)):
    return crud.product.get_products(db)


@router.get("/{product_id}", response_model=schemas.ProductOut)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.product.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=schemas.ProductOut)
def update_product(product_id: int, product_data: schemas.ProductUpdate, db: Session = Depends(get_db)):
    product = crud.product.update_product(db, product_id, product_data)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.delete("/{product_id}", status_code=200)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    deleted = crud.product.get_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    crud.product.delete_product(db, product_id)
    return {"message": "Product deleted successfully"}

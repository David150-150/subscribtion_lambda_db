# flake8: noqa: F401
from typing import List, Optional

from sqlalchemy.orm import Session

from app import schemas
from app.models import Product
from app.schemas.product import ProductBase


# -----------------CREATE PRODUCT------------#
def create_product(db: Session, product: schemas.ProductBase) -> Product:
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


# -----------------GET ALL PRODUCT------------#
def get_products(db: Session) -> List[Product]:
    return db.query(Product).all()


# -----------------GET PRODUCT------------#
def get_product(db: Session, product_id: int) -> Optional[Product]:
    return db.query(Product).filter(Product.product_id == product_id).first()


# -----------------UPDATE PRODUCT------------#
def update_product(db: Session, product_id: int, product_data: schemas.ProductUpdate) -> Optional[Product]:
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        return None

    # Only update fields that were provided
    for key, value in product_data.dict(exclude_unset=True).items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


# -----------------DELETE PRODUCT------------#
def delete_product(db: Session, product_id: int) -> Optional[Product]:
    product = db.query(Product).filter(Product.product_id == product_id).first()

    if product:
        db.delete(product)
        db.commit()
        return product
    return None

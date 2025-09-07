from sqlalchemy import DECIMAL, TIMESTAMP, Column, Integer, String
from sqlalchemy.sql import func

from app.db import Base


# --------------CREATE PRODUCT TABLE-------------------#
class Product(Base):
    __tablename__ = "product"

    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), unique=True, nullable=False)
    description = Column(String(100), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

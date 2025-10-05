# # app/db.py
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.settings import settings

# Use TEST_DATABASE_URL if TESTING is set, otherwise use normal DATABASE_URL
DATABASE_URL = os.getenv("TEST_DATABASE_URL") or settings.DATABASE_URL

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

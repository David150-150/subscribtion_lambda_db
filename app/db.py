# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
# from app.settings import settings
# import os


# DATABASE_URL = settings.DATABASE_URL

# # Create engine with echo enabled (optional, for debugging SQL queries)
# engine = create_engine(DATABASE_URL, echo=False)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

# # Dependency for FastAPI
# from sqlalchemy.orm import Session

# def get_db():
#     db: Session = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()




# app/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from app.settings import settings

# Database URL from settings.py (.env)
DATABASE_URL = settings.DATABASE_URL

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=False)  # Set echo=True to debug SQL queries

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency for FastAPI routes
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

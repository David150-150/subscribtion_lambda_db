# flake8: noqa: F401,F841
# app/create_tables.py
import sys

from sqlalchemy.exc import OperationalError

from app import models  # Import all your models to register them with Base
from app.db import Base, engine  # db.py contains Base and engine


def create_all_tables():
    try:
        # Test database connection
        with engine.connect() as conn:
            print("Successfully connected to the database.")

        # Create all tables
        print("Creating all tables...")
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully!")

    except OperationalError as e:
        print("ERROR: Could not connect to the database.")
        print(str(e))
        sys.exit(1)


if __name__ == "__main__":
    create_all_tables()

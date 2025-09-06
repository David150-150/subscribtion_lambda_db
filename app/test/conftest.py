# ------------------Imported all my necessary imports------------------#
import os
from dotenv import load_dotenv
load_dotenv()
import pytest 
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base, get_db
from app.main import app

# ------------------Set up my DB configuration------------------#
#TEST_DATABASE_URL = "mysql+mysqlconnector://root:newpass123@127.0.0.1:3306/SubscribDB"
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ------------------Set up my DB Dependency------------------#
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------Override my Dependency------------------#
app.dependency_overrides[get_db] = override_get_db

# ------------------Create and drop my testing tables------------------#
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # ---------Ensure all tables are dropped before test starts--------#
    Base.metadata.drop_all(bind=engine)
    # ---------Create fresh tables before test run--------#
    Base.metadata.create_all(bind=engine)
    yield
    # ---------Clean up: Drop all tables after test session ends--------#
    Base.metadata.drop_all(bind=engine)

# ------------------Provide my TestClient------------------#
@pytest.fixture()
def client():
    with TestClient(app) as client:
        yield client






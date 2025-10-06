# flake8: noqa: E402
# flake8: noqa: F401,F841,E501
import os
import uuid

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.db import Base, get_db
from app.main import app


# Helper to safely truncate passwords to 72 bytes
def safe_password(pwd: str) -> str:
    return pwd.encode("utf-8")[:72].decode("utf-8", "ignore")


load_dotenv()

# ------------------Database setup------------------#
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ------------------Dependency override------------------#
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# ------------------Database fixtures------------------#
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create tables before any tests run."""
    print("Setting up the test database...")

    from app.models.customer import Customer
    from app.models.product import Product
    from app.models.schedule import Schedule
    from app.models.subscription import Subscription
    from app.models.transaction import Transaction
    from app.models.transaction_details import TransactionDetails
    from app.models.transaction_failures import TransactionFailures

    Base.metadata.create_all(bind=engine)
    print("All tables are ready.")
    yield
    # Optional: drop tables after tests if you want a completely clean DB
    # Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
def clean_database():
    """Truncate relevant tables before each test to prevent duplicates."""
    with engine.connect() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS=0;"))
        conn.execute(text("TRUNCATE TABLE subscription;"))
        conn.execute(text("TRUNCATE TABLE customer;"))
        conn.execute(text("TRUNCATE TABLE product;"))
        # Add other tables if necessary
        conn.execute(text("SET FOREIGN_KEY_CHECKS=1;"))
        conn.commit()
    yield


# ------------------Test client------------------#
@pytest.fixture()
def client():
    with TestClient(app) as client:
        yield client


# ------------------Reusable fixtures for creating entities------------------#
@pytest.fixture
def create_customer(client):
    def _create_customer(
        first_name="Test",
        middle_name="",
        last_name="User",
        email=None,
        telephone="0551234567",
        password="strongpass123",
    ):
        if email is None:
            email = f"test_{uuid.uuid4().hex[:6]}@example.com"

        # Truncate password safely
        password = safe_password(password)

        response = client.post(
            "/customer/",
            json={
                "first_name": first_name,
                "middle_name": middle_name,
                "last_name": last_name,
                "email": email,
                "telephone": telephone,
                "password": password,
            },
        )
        print(response.json())  # Debugging
        return response.json()["customer_id"]

    return _create_customer


@pytest.fixture
def create_product(client):
    def _create_product(name=None, description="Description", price="100.0"):
        if name is None:
            name = f"Test Product {uuid.uuid4().hex[:6]}"  # unique name

        response = client.post(
            "/product/",
            json={"name": name, "description": description, "price": price},
        )
        print(response.json())  # Debugging
        return response.json()["product_id"]

    return _create_product


@pytest.fixture
def create_subscription(client, create_customer, create_product):
    def _create_subscription(status="active"):
        customer_id = create_customer()
        product_id = create_product()
        response = client.post(
            "/subscription/",
            json={
                "customer_id": customer_id,
                "product_id": product_id,
                "status": status,
            },
        )
        return response.json()["subscription_id"]

    return _create_subscription


@pytest.fixture
def create_transaction(client, create_subscription):
    def _create_transaction():
        subscription_id = create_subscription()
        response = client.post("/transaction/", json={"subscription_id": subscription_id})
        return response.json()["transaction_id"]

    return _create_transaction


@pytest.fixture
def create_transaction_detail(client, create_transaction):
    def _create_transaction_detail():
        transaction_id = create_transaction()
        response = client.post(
            "/transaction-detail/",
            json={
                "transaction_id": transaction_id,
                "action_task": "Billing",
                "status": "successful",
                "message": "Billed successfully",
            },
        )
        return response.json()["transaction_details_id"]

    return _create_transaction_detail


@pytest.fixture
def create_transaction_failure(client, create_transaction):
    def _create_transaction_failure():
        transaction_id = create_transaction()
        response = client.post(
            "/transaction_failures/",
            json={"transaction_id": transaction_id, "failure_reason": "Card declined"},
        )
        return response.json()["transaction_failure_id"]

    return _create_transaction_failure


@pytest.fixture
def create_schedule(client, create_subscription):
    def _create_schedule(task_name="Default Task", status="pending"):
        subscription_id = create_subscription()
        response = client.post(
            "/schedule/",
            json={
                "subscription_id": subscription_id,
                "task_name": task_name,
                "status": status,
            },
        )
        return response.json()["schedule_id"]

    return _create_schedule


# ------------------Negative / edge-case fixtures------------------#
@pytest.fixture
def create_invalid_customer(client):
    """Attempts to create a customer with invalid data."""

    def _create_invalid_customer(
        first_name="",
        last_name="",
        email="not-an-email",
        telephone="abc",
        password="123",
    ):
        response = client.post(
            "/customer/",
            json={
                "first_name": first_name,
                "middle_name": "",
                "last_name": last_name,
                "email": email,
                "telephone": telephone,
                "password": password,
            },
        )
        return response

    return _create_invalid_customer


@pytest.fixture
def create_duplicate_customer(client, create_customer):
    """Attempts to create a customer with an email that already exists."""

    def _create_duplicate_customer():
        customer_id = create_customer()
        response = client.post(
            "/customer/",
            json={
                "first_name": "Duplicate",
                "middle_name": "",
                "last_name": "User",
                "email": f"test_{uuid.uuid4().hex[:6]}@example.com",  # simulate duplicate email
                "telephone": "0550000000",
                "password": "strongpass123",
            },
        )
        return response

    return _create_duplicate_customer


@pytest.fixture
def create_invalid_product(client):
    """Attempts to create a product with invalid data."""

    def _create_invalid_product(name="", description="", price=-100):
        response = client.post(
            "/product/",
            json={"name": name, "description": description, "price": price},
        )
        return response

    return _create_invalid_product


@pytest.fixture
def delete_nonexistent_customer(client):
    """Attempts to delete a customer that does not exist."""

    def _delete_nonexistent_customer(customer_id=999999):
        response = client.delete(f"/customer/{customer_id}")
        return response

    return _delete_nonexistent_customer


@pytest.fixture
def delete_nonexistent_product(client):
    """Attempts to delete a product that does not exist."""

    def _delete_nonexistent_product(product_id=999999):
        response = client.delete(f"/product/{product_id}")
        return response

    return _delete_nonexistent_product

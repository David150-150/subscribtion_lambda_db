# flake8: noqa: F401,F841,E501
import uuid

import pytest


# ---------------- SIGNUP TESTS ---------------- #
def test_signup_success(client):
    response = client.post("/auth/signup", json={"first_name": "John", "middle_name": "A", "last_name": "Doe", "email": "john_doe@example.com", "telephone": "0551234567", "password": "strongpass123"})
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["first_name"] == "John"
    assert "customer_id" in data


def test_signup_existing_email(client, create_customer):
    email = f"existing_{uuid.uuid4().hex[:6]}@example.com"
    create_customer(email=email)
    response = client.post("/auth/signup", json={"first_name": "Jane", "middle_name": "B", "last_name": "Smith", "email": email, "telephone": "0557654321", "password": "anotherpass123"})
    # Expecting a 400 or 409 depending on your API handling
    assert response.status_code in [400, 409]


# ---------------- LOGIN TESTS ---------------- #
def test_login_success(client, create_customer):
    email = f"login_{uuid.uuid4().hex[:6]}@example.com"
    password = "strongpass123"
    create_customer(email=email, password=password)
    response = client.post("/auth/login", data={"email": email, "password": password})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, create_customer):
    email = f"wrongpass_{uuid.uuid4().hex[:6]}@example.com"
    password = "strongpass123"
    create_customer(email=email, password=password)
    response = client.post("/auth/login", data={"email": email, "password": "incorrect"})
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    response = client.post("/auth/login", data={"email": "nonexistent@example.com", "password": "nopass123"})
    assert response.status_code == 401

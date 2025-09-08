# flake8: noqa: F401,F841,E501

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_signup():
    response = client.post(
        "/auth/signup",
        json={
            "first_name": "David",
            "middle_name": "",
            "last_name": "Kusi",
            "email": "david@gmail.com",
            "telephone": "0551234567",
            "password": "strongpass123",
        },
    )

    assert response.status_code == 200 or response.status_code == 201
    data = response.json()
    assert data["email"] == "david@gmail.com"
    assert "customer_id" in data
    assert "password" not in data  # Password should not be returned


def test_login():
    response = client.post(
        "/auth/login",
        data={
            "username": "david@gmail.com",  # OAuth2PasswordRequestForm uses "username" key
            "password": "strongpass123",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_password():
    response = client.post(
        "/auth/login",
        data={
            "username": "david@gmail.com",
            "password": "trongpass123",  # wrong password
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_login_nonexistent_user():
    response = client.post("/auth/login", data={"username": "rice@gmail.com", "password": "Ricepass000"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

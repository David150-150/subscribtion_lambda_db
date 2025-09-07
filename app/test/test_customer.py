# flake8: noqa: F401,F841,E501

# tests/test_customer.py
import pytest


def test_create_customer(client):
    response = client.post(
        "/customer/", json={"name": "Ama Budu", "email": "Budu@gmail.com"}
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Ama Budu"
    assert "customer_id" in response.json()


def test_get_customers(client):
    response = client.get("/customer/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_customer(client):
    # First, create a customer
    create = client.post(
        "/customer/", json={"name": "Ama Buudu", "email": "Buudu@gmail.com"}
    )

    customer_id = create.json()["customer_id"]

    # Now get that customer
    response = client.get(f"/customer/{customer_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Ama Buudu"
    assert response.json()["email"] == "Buudu@gmail.com"


def test_update_customer(client):
    create = client.post(
        "/customer/", json={"name": "Ama Moom", "email": "Moom@gmail.com"}
    )

    customer_id = create.json()["customer_id"]
    response = client.put(
        f"/customer/{customer_id}",
        json={"name": "Kuku Bonsu", "email": "kuku@gmail.com"},
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Kuku Bonsu"
    assert response.json()["email"] == "kuku@gmail.com"
    # Cleanup: delete test customer
    client.delete(f"/customer/{customer_id}")


def test_delete_customer(client):
    create = client.post(
        "/customer/", json={"name": "Kuku Bonsu", "email": "Bonsu@gmail.com"}
    )

    customer_id = create.json()["customer_id"]

    response = client.delete(f"/customer/{customer_id}")
    assert response.status_code == 200

    # Confirm deletion
    follow_up = client.get(f"/customer/{customer_id}")
    assert follow_up.status_code == 404

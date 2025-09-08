# flake8: noqa: F401,F841,E501

from datetime import date

import pytest


def test_create_schedule(client):
    # Create a customer
    customer = client.post("/customer/", json={"name": "David", "email": "david@gmail.com.com"})
    customer_id = customer.json()["customer_id"]

    # Create a product
    product = client.post(
        "/product/",
        json={"name": "Boss Package", "description": "One for all", "price": "700.99"},
    )
    product_id = product.json()["product_id"]

    # Create a subscription
    subscription = client.post("/subscription/", json={"customer_id": 1, "product_id": 1, "status": "active"})
    subscription_id = subscription.json()["subscription_id"]

    # Create a schedule
    response = client.post(
        "/schedule/",
        json={
            "subscription_id": 1,
            "task_name": "upgradeing package",
            "status": "pending",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["task_name"] == "upgrading"
    assert data["status"] == "pending"


def test_get_schedules(client):
    response = client.get("/schedule/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_single_schedule(client):
    # Create a schedule
    sub = client.get("/subscription/").json()[0]
    response = client.post(
        "/schedule/",
        json={"subscription_id": sub["subscription_id"], "task_name": "Follow-up Task"},
    )
    schedule_id = response.json()["schedule_id"]

    # Get it
    response = client.get(f"/schedule/{schedule_id}")
    assert response.status_code == 200
    assert response.json()["task_name"] == "Follow-up Task"


def test_update_schedule(client):
    # Create a schedule
    sub = client.get("/subscription/").json()[0]
    response = client.post(
        "/schedule/",
        json={"subscription_id": sub["subscription_id"], "task_name": "To Update"},
    )
    schedule_id = response.json()["schedule_id"]

    # Update
    response = client.put(f"/schedule/{schedule_id}", json={"status": "complete"})
    assert response.status_code == 200
    assert response.json()["status"] == "complete"


def test_delete_schedule(client):
    # Create a schedule
    sub = client.get("/subscription/").json()[0]
    response = client.post(
        "/schedule/",
        json={"subscription_id": sub["subscription_id"], "task_name": "To Delete"},
    )
    schedule_id = response.json()["schedule_id"]

    # Delete
    response = client.delete(f"/schedule/{schedule_id}")
    assert response.status_code == 200

    # Confirm deletion
    follow_up = client.get(f"/schedule/{schedule_id}")
    assert follow_up.status_code == 404

# flake8: noqa: F401,F841,E501
import pytest


def test_create_subscription_success(client, create_customer, create_product):
    customer_id = create_customer()
    product_id = create_product()
    response = client.post(
        "/subscription/",
        json={"customer_id": customer_id, "product_id": product_id, "status": "active"},
    )
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["customer_id"] == customer_id
    assert data["product_id"] == product_id
    assert data["status"] == "active"


def test_create_subscription_invalid_status(client, create_customer, create_product):
    customer_id = create_customer()
    product_id = create_product()
    response = client.post(
        "/subscription/",
        json={
            "customer_id": customer_id,
            "product_id": product_id,
            "status": "wrong_status",
        },
    )
    assert response.status_code == 422  # validation error


def test_get_subscription_success(client, create_subscription):
    subscription_id = create_subscription()
    response = client.get(f"/subscription/{subscription_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["subscription_id"] == subscription_id


def test_get_subscription_not_found(client):
    response = client.get("/subscription/999999")
    assert response.status_code == 404


def test_get_all_subscriptions(client, create_subscription):
    create_subscription()
    create_subscription()
    response = client.get("/subscription/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_update_subscription_success(client, create_subscription):
    subscription_id = create_subscription()
    response = client.put(f"/subscription/{subscription_id}", json={"status": "inactive"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "inactive"


def test_update_subscription_not_found(client):
    response = client.put("/subscription/999999", json={"status": "cancelled"})
    assert response.status_code == 404


def test_delete_subscription_success(client, create_subscription):
    subscription_id = create_subscription()
    response = client.delete(f"/subscription/{subscription_id}")
    assert response.status_code == 200
    follow_up = client.get(f"/subscription/{subscription_id}")
    assert follow_up.status_code == 404


def test_delete_subscription_not_found(client):
    response = client.delete("/subscription/999999")
    assert response.status_code == 404

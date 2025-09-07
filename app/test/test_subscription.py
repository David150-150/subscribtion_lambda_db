# flake8: noqa: F401,F841,E501

import pytest


def create_customer_and_product(client):
    # Create customer
    customer = client.post(
        "/customer/", json={"name": "John", "email": "john@gmail.com"}
    )
    customer_id = customer.json()["customer_id"]

    # Create product
    product = client.post(
        "/product/",
        json={"name": "small pack", "description": "This is less", "price": "49.99"},
    )
    product_id = product.json()["product_id"]

    return customer_id, product_id


# CREATE
def test_create_subscription(client):
    customer_id, product_id = create_customer_and_product(client)
    response = client.post(
        "/subscription/", json={"customer_id": 1, "product_id": 1, "status": "active"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["customer_id"] == 1
    assert data["product_id"] == 1
    assert data["status"] == "active"
    assert "subscription_id" in data


# GET BY ID
def test_get_subscription(client):
    customer_id, product_id = create_customer_and_product(client)
    create = client.post(
        "/subscription/", json={"customer_id": 1, "product_id": 2, "status": "active"}
    )
    sub_id = create.json()["subscription_id"]

    response = client.get(f"/subscription/{sub_id}")
    assert response.status_code == 200
    assert response.json()["subscription_id"] == sub_id


# GET ALL
def test_get_subscriptions(client):
    customer_id, product_id = create_customer_and_product(client)
    client.post(
        "/subscription/", json={"customer_id": 1, "product_id": 1, "status": "active"}
    )
    client.post(
        "/subscription/", json={"customer_id": 1, "product_id": 2, "status": "inactive"}
    )

    response = client.get("/subscription/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    for sub in data:
        assert "subscription_id" in sub
        assert sub["status"] in ["active", "inactive", "cancelled"]


# UPDATE
def test_update_subscription(client):
    customer_id, product_id = create_customer_and_product(client)
    create = client.post(
        "/subscription/", json={"customer_id": 1, "product_id": 2, "status": "active"}
    )
    sub_id = create.json()["subscription_id"]

    response = client.put(f"/subscription/{sub_id}", json={"status": "cancelled"})
    assert response.status_code == 200
    assert response.json()["status"] == "cancelled"


# DELETE
def test_delete_subscription(client):
    customer_id, product_id = create_customer_and_product(client)
    create = client.post(
        "/subscription/", json={"customer_id": 1, "product_id": 2, "status": "active"}
    )
    sub_id = create.json()["subscription_id"]

    response = client.delete(f"/subscription/{sub_id}")
    assert response.status_code == 200

    # Confirm it's deleted
    check = client.get(f"/subscription/{sub_id}")
    assert check.status_code == 404

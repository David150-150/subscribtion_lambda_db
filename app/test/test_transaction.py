# flake8: noqa: F401,F841,E501

import pytest


# CREATE
def test_create_transaction(client):
    # Ensure subscription exists
    subscription = client.post(
        "/subscription/", json={"customer_id": 1, "product_id": 1, "status": "active"}
    )
    sub_id = subscription.json()["subscription_id"]

    # Create transaction
    response = client.post("/transaction/", json={"subscription_id": 1})
    assert response.status_code == 201
    data = response.json()
    assert data["subscription_id"] == 1
    assert "transaction_id" in data
    assert "created_at" in data


# GET BY ID
def test_get_transaction(client):
    sub = client.post(
        "/subscription/", json={"customer_id": 1, "product_id": 1, "status": "active"}
    )
    sub_id = sub.json()["subscription_id"]

    txn = client.post("/transaction/", json={"subscription_id": sub_id})
    txn_id = txn.json()["transaction_id"]

    response = client.get(f"/transaction/{txn_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["transaction_id"] == 1
    assert data["subscription_id"] == 1


# GET ALL
def test_get_transactions(client):
    sub = client.post(
        "/subscription/", json={"customer_id": 1, "product_id": 1, "status": "active"}
    )
    sub_id = sub.json()["subscription_id"]

    client.post("/transaction/", json={"subscription_id": sub_id})
    client.post("/transaction/", json={"subscription_id": sub_id})

    response = client.get("/transaction/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    for txn in data:
        assert "transaction_id" in txn
        assert "subscription_id" in txn
        assert "created_at" in txn


# DELETE
def test_delete_transaction(client):
    sub = client.post(
        "/subscription/", json={"customer_id": 1, "product_id": 1, "status": "active"}
    )
    sub_id = sub.json()["subscription_id"]

    txn = client.post("/transaction/", json={"subscription_id": sub_id})
    txn_id = txn.json()["transaction_id"]

    response = client.delete(f"/transaction/{txn_id}")
    assert response.status_code == 200

    # Confirm deletion
    check = client.get(f"/transaction/{txn_id}")
    assert check.status_code == 404

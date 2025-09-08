# flake8: noqa: F401,F841,E501

import pytest


# CREATE
def test_create_transaction_failure(client):
    transaction = client.post("/transaction/", json={"subscription_id": 1})
    transaction_id = transaction.json()["transaction_id"]

    response = client.post(
        "/transaction-failure/",
        json={"transaction_id": 1, "failure_reason": "Card declined"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["transaction_id"] == transaction_id
    assert data["failure_reason"] == "Card declined"
    assert "transaction_failure_id" in data
    assert "failed_at" in data


# GET BY ID
def test_get_transaction_failure(client):
    create = client.post("/transaction-failure/", json={"transaction_id": 1, "failure_reason": "Timeout"})
    failure_id = create.json()["transaction_failure_id"]

    response = client.get(f"/transaction-failure/{failure_id}")
    assert response.status_code == 200
    assert response.json()["transaction_failure_id"] == failure_id


# GET ALL
def test_get_all_transaction_failures(client):
    response = client.get("/transaction-failure/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

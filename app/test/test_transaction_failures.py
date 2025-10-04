# flake8: noqa: F401,F841,E501

import pytest


def test_create_transaction_failure_success(client, create_transaction):
    transaction_id = create_transaction()
    response = client.post("/transaction_failures/", json={"transaction_id": transaction_id, "failure_reason": "Card declined"})
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["transaction_id"] == transaction_id
    assert data["failure_reason"] == "Card declined"


def test_get_transaction_failure_success(client, create_transaction_failure):
    failure_id = create_transaction_failure()
    response = client.get(f"/transaction_failures/{failure_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["transaction_failure_id"] == failure_id


def test_get_transaction_failure_not_found(client):
    response = client.get("/transaction_failures/999999")
    assert response.status_code == 404


def test_get_all_transaction_failures(client, create_transaction_failure):
    create_transaction_failure()
    create_transaction_failure()
    response = client.get("/transaction_failures/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2

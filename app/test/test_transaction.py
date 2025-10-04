# flake8: noqa: F401,F841,E501
import pytest


def test_create_transaction_success(client, create_subscription):
    subscription_id = create_subscription()
    response = client.post("/transaction/", json={"subscription_id": subscription_id})
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["subscription_id"] == subscription_id
    assert "transaction_id" in data


def test_get_transaction_success(client, create_transaction):
    transaction_id = create_transaction()
    response = client.get(f"/transaction/{transaction_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["transaction_id"] == transaction_id


def test_get_transaction_not_found(client):
    response = client.get("/transaction/999999")
    assert response.status_code == 404


def test_get_all_transactions(client, create_transaction):
    create_transaction()
    create_transaction()
    response = client.get("/transaction/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_delete_transaction_success(client, create_transaction):
    transaction_id = create_transaction()
    response = client.delete(f"/transaction/{transaction_id}")
    assert response.status_code == 200
    follow_up = client.get(f"/transaction/{transaction_id}")
    assert follow_up.status_code == 404


def test_delete_transaction_not_found(client):
    response = client.delete("/transaction/999999")
    assert response.status_code == 404

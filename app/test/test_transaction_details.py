# flake8: noqa: F401,F841,E501
import pytest


def test_create_transaction_detail_success(client, create_transaction):
    transaction_id = create_transaction()
    response = client.post(
        "/transaction-detail/",
        json={
            "transaction_id": transaction_id,
            "action_task": "Billing",
            "status": "successful",
            "message": "Billed successfully",
        },
    )
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["transaction_id"] == transaction_id
    assert data["status"] == "successful"


def test_get_transaction_detail_success(client, create_transaction_detail):
    details_id = create_transaction_detail()
    response = client.get(f"/transaction-detail/{details_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["transaction_details_id"] == details_id


def test_get_transaction_detail_not_found(client):
    response = client.get("/transaction-detail/999999")
    assert response.status_code == 404


def test_get_all_transaction_details(client, create_transaction_detail):
    create_transaction_detail()
    create_transaction_detail()
    response = client.get("/transaction-detail/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2

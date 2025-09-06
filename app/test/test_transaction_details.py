import pytest

# CREATE
def test_create_transaction_detail(client):
    # Ensure at least one transaction exists
    transaction = client.post("/transaction/", json={"subscription_id": 1})
    transaction_id = transaction.json()["transaction_id"]

    response = client.post("/transaction-detail/", json={
        "transaction_id": 3,
        "action_task": "Billing",
        "status": "successful",
        "message": "Billed successfully"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["transaction_id"] == transaction_id
    assert data["action_task"] == "Billing"
    assert data["status"] == "successful"
    assert "transaction_details_id" in data

# GET BY ID
def test_get_transaction_detail(client):
    create = client.post("/transaction-detail/", json={
        "transaction_id": 1,
        "action_task": "Verify payment",
        "status": "successful",
        "message": "Verified"
    })
    detail_id = create.json()["transaction_details_id"]

    response = client.get(f"/transaction-detail/{detail_id}")
    assert response.status_code == 200
    assert response.json()["transaction_details_id"] == detail_id

# GET ALL
def test_get_all_transaction_details(client):
    response = client.get("/transaction-detail/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

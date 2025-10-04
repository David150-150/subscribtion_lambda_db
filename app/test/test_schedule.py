# flake8: noqa: F401,F841,E501

import pytest


def test_create_schedule_success(client, create_subscription):
    subscription_id = create_subscription()
    response = client.post(
        "/schedule/",
        json={
            "subscription_id": subscription_id,
            "task_name": "Test Task",
            "status": "pending",
        },
    )
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["task_name"] == "Test Task"
    assert data["subscription_id"] == subscription_id
    assert "schedule_id" in data


def test_create_schedule_invalid_status(client, create_subscription):
    subscription_id = create_subscription()
    response = client.post(
        "/schedule/",
        json={
            "subscription_id": subscription_id,
            "task_name": "Invalid Task",
            "status": "wrong_status",
        },
    )
    assert response.status_code == 422  # validation error


def test_get_schedule_success(client, create_schedule):
    schedule_id = create_schedule()
    response = client.get(f"/schedule/{schedule_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["schedule_id"] == schedule_id


def test_get_schedule_not_found(client):
    response = client.get("/schedule/999999")
    assert response.status_code == 404


def test_get_all_schedules(client, create_schedule):
    create_schedule()
    create_schedule()
    response = client.get("/schedule/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_update_schedule_success(client, create_schedule):
    schedule_id = create_schedule()
    response = client.put(f"/schedule/{schedule_id}", json={"status": "complete"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "complete"


def test_update_schedule_not_found(client):
    response = client.put("/schedule/999999", json={"status": "cancelled"})
    assert response.status_code == 404


def test_delete_schedule_success(client, create_schedule):
    schedule_id = create_schedule()
    response = client.delete(f"/schedule/{schedule_id}")
    assert response.status_code == 200
    follow_up = client.get(f"/schedule/{schedule_id}")
    assert follow_up.status_code == 404


def test_delete_schedule_not_found(client):
    response = client.delete("/schedule/999999")
    assert response.status_code == 404

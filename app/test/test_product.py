# flake8: noqa: F401,F841,E501
import pytest


def test_create_product_success(client):
    response = client.post(
        "/product/",
        json={"name": "Basic Plan", "description": "Test product", "price": 100.0},
    )
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["name"] == "Basic Plan"
    assert "product_id" in data


def test_get_product_success(client, create_product):
    product_id = create_product()
    response = client.get(f"/product/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == product_id


def test_get_product_not_found(client):
    response = client.get("/product/999999")
    assert response.status_code == 404


def test_get_all_products(client, create_product):
    create_product()
    create_product()
    response = client.get("/product/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_update_product_success(client, create_product):
    product_id = create_product()
    response = client.put(
        f"/product/{product_id}",
        json={"name": "Updated Product", "description": "Updated", "price": 199.99},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Product"


def test_update_product_not_found(client):
    response = client.put("/product/999999", json={"name": "Nobody"})
    assert response.status_code == 404


def test_delete_product_success(client, create_product):
    product_id = create_product()
    response = client.delete(f"/product/{product_id}")
    assert response.status_code == 200
    follow_up = client.get(f"/product/{product_id}")
    assert follow_up.status_code == 404


def test_delete_product_not_found(client):
    response = client.delete("/product/999999")
    assert response.status_code == 404

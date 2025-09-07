# flake8: noqa: F401,F841,E501

# tests/test_product.py
import pytest


def test_create_product(client):
    response = client.post(
        "/product/",
        json={
            "name": "Sports Plus",
            "description": "This subscription comes with all your favorite channels",
            "price": "250.68",
        },
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Sports Plus"
    assert "product_id" in response.json()


def test_get_products(client):
    response = client.get("/product/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_product(client):
    # First, create a product
    create = client.post(
        "/product/",
        json={
            "name": "Boss Plan",
            "description": "The Boss package",
            "price": "300.00",
        },
    )
    assert create.status_code == 200
    product_id = create.json()["product_id"]

    # Now fetch it
    response = client.get(f"/product/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Boss Plan"


def test_update_product(client):
    # Create product to update
    create = client.post(
        "/product/",
        json={
            "name": "Mid Boss",
            "description": "Initial Description",
            "price": "99.99",
        },
    )
    product_id = create.json()["product_id"]

    # Update it
    response = client.put(
        f"/product/{product_id}",
        json={
            "name": "Boss Package",
            "description": "This is a mega pack",
            "price": "199.99",
        },
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Boss Package"


def test_delete_product(client):
    create = client.post(
        "/product/",
        json={
            "name": "Big Package",
            "description": "This is a mega pack",
            "price": "199.99",
        },
    )

    product_id = create.json()["product_id"]

    response = client.delete(f"/product/{product_id}")
    assert response.status_code == 200

    # Confirm deletion
    follow_up = client.get(f"/product/{product_id}")
    assert follow_up.status_code == 404

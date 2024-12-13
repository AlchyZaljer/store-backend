import pytest


@pytest.mark.usefixtures("override_get_db")
def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Glossary Service API"}


@pytest.mark.usefixtures("override_get_db")
def test_create_product(client, product_data):
    response = client.post("/products/", json=product_data)
    assert response.status_code == 200
    assert response.json()["name"] == product_data["name"]
    assert response.json()["price"] == product_data["price"]


@pytest.mark.usefixtures("override_get_db")
def test_get_product(client, product_data):
    create_response = client.post("/products/", json=product_data)
    product_id = create_response.json()["id"]

    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["id"] == product_id
    assert response.json()["name"] == product_data["name"]


@pytest.mark.usefixtures("override_get_db")
def test_list_products(client, product_data):
    client.post("/products/", json=product_data)

    response = client.get("/products/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == product_data["name"]


@pytest.mark.usefixtures("override_get_db")
def test_update_product(client, product_data):
    create_response = client.post("/products/", json=product_data)
    product_id = create_response.json()["id"]

    update_data = {"price": 12.99, "description": "Updated test product"}
    update_response = client.patch(f"/products/{product_id}", json=update_data)
    assert update_response.status_code == 200
    assert update_response.json()["price"] == 12.99
    assert update_response.json()["description"] == "Updated test product"


@pytest.mark.usefixtures("override_get_db")
def test_delete_product(client, product_data):
    create_response = client.post("/products/", json=product_data)
    product_id = create_response.json()["id"]

    remove_response = client.delete(f"/products/{product_id}")
    assert remove_response.status_code == 200
    assert remove_response.json()["message"] == f"Product {product_id} deleted"

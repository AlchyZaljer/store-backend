import pytest


@pytest.mark.usefixtures("override_get_db")
def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Product Service API"}


@pytest.mark.usefixtures("override_get_db")
def test_create_product(client, product_data):
    response = client.post("/products/", json=product_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"
    assert response.json()["price"] == 10.99


@pytest.mark.usefixtures("override_get_db")
def test_get_product(client, product_data):
    create_response = client.post("/products/", json=product_data)
    product_id = create_response.json()["id"]

    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["id"] == product_id
    assert response.json()["name"] == "Test Product"


@pytest.mark.usefixtures("override_get_db")
def test_list_products(client):
    response = client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.usefixtures("override_get_db")
def test_update_product(client, product_data):
    create_response = client.post("/products/", json=product_data)
    product_id = create_response.json()["id"]

    update_data = {"price": 12.99}
    response = client.patch(f"/products/{product_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["price"] == 12.99


@pytest.mark.usefixtures("override_get_db")
def test_delete_product(client, product_data):
    create_response = client.post("/products/", json=product_data)
    product_id = create_response.json()["id"]

    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Product {product_id} deleted"

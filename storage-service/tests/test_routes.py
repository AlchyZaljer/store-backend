import pytest


@pytest.mark.usefixtures("override_get_db")
def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Storage Service API"}


@pytest.mark.usefixtures("override_get_db", "mock_is_product_exist")
def test_add_item(client, test_item_data):
    response = client.post("/items/add/", json=test_item_data)
    assert response.status_code == 200
    assert response.json()["product_id"] == test_item_data["product_id"]
    assert response.json()["quantity"] == test_item_data["quantity"]


@pytest.mark.usefixtures("override_get_db", "mock_is_product_exist")
def test_get_item(client, test_item_data):
    add_response = client.post("/items/add/", json=test_item_data)
    product_id = add_response.json()["product_id"]

    response = client.get(f"/items/{product_id}")
    assert response.status_code == 200
    assert response.json()["product_id"] == test_item_data["product_id"]
    assert response.json()["quantity"] == test_item_data["quantity"]


@pytest.mark.usefixtures("override_get_db", "mock_is_product_exist")
def test_list_items(client, test_item_data):
    client.post("/items/add/", json=test_item_data)

    response = client.get("/items/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["product_id"] == test_item_data["product_id"]


@pytest.mark.usefixtures("override_get_db", "mock_is_product_exist")
def test_update_items(client, test_item_data):
    add_response = client.post("/items/add/", json=test_item_data)
    product_id = add_response.json()["product_id"]

    update_data = [{"product_id": product_id, "quantity": 20}]
    update_response = client.patch(f"/items/", json=update_data)
    assert update_response.status_code == 200

    updated_items = update_response.json()
    assert updated_items[0]["product_id"] == product_id
    assert updated_items[0]["quantity"] == 20


@pytest.mark.usefixtures("override_get_db", "mock_is_product_exist")
def test_remove_item(client, test_item_data):
    add_response = client.post("/items/add/", json=test_item_data)
    product_id = add_response.json()["product_id"]
    initial_quantity = add_response.json()["quantity"]

    remove_data = {"product_id": product_id, "quantity": 5}
    remove_response = client.post("/items/remove/", json=remove_data)
    assert remove_response.status_code == 200
    assert remove_response.json()["quantity"] == initial_quantity - 5

    remove_data = {"product_id": product_id, "quantity": initial_quantity - 5}
    remove_response = client.post("/items/remove/", json=remove_data)
    assert remove_response.status_code == 200
    assert remove_response.json()["message"] == f"Product {product_id} deleted"


@pytest.mark.usefixtures("override_get_db", "mock_is_product_exist")
def test_reserve_items(client, test_item_data):
    add_response = client.post("/items/add/", json=test_item_data)
    product_id = add_response.json()["product_id"]
    initial_quantity = add_response.json()["quantity"]

    reserve_data = [{"product_id": product_id, "quantity": 5}]
    reserve_response = client.post("/reserve/", json=reserve_data)
    assert reserve_response.status_code == 200
    assert reserve_response.json()["message"] == "Items reserved successfully"

    get_response = client.get(f"/items/{product_id}")
    assert get_response.status_code == 200
    assert get_response.json()["quantity"] == initial_quantity - 5

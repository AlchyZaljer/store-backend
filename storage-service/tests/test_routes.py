import pytest


@pytest.mark.usefixtures("override_get_db")
def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Storage Service API"}


@pytest.mark.usefixtures("override_get_db")
def test_add_item(client, test_item_data):
    response = client.post("/items/add/", json=test_item_data)
    assert response.status_code == 200
    assert response.json()["name"] == test_item_data["name"]
    assert response.json()["quantity"] == test_item_data["quantity"]
    assert response.json()["price"] == test_item_data["price"]


@pytest.mark.usefixtures("override_get_db")
def test_get_item_by_id(client, test_item_data):
    add_response = client.post("/items/add/", json=test_item_data)
    item_id = add_response.json()["id"]

    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["id"] == item_id
    assert response.json()["name"] == test_item_data["name"]


@pytest.mark.usefixtures("override_get_db")
def test_list_items(client, test_item_data):
    client.post("/items/add/", json=test_item_data)

    response = client.get("/items/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == test_item_data["name"]


@pytest.mark.usefixtures("override_get_db")
def test_update_item(client, test_item_data):
    add_response = client.post("/items/add/", json=test_item_data)
    item_id = add_response.json()["id"]

    update_data = {"price": 120.99, "description": "Updated test item"}
    update_response = client.patch(f"/items/{item_id}", json=update_data)
    assert update_response.status_code == 200
    assert update_response.json()["price"] == 120.99
    assert update_response.json()["description"] == "Updated test item"


@pytest.mark.usefixtures("override_get_db")
def test_remove_item(client, test_item_data):
    add_response = client.post("/items/add/", json=test_item_data)
    item_id = add_response.json()["id"]

    remove_response = client.post(f"/items/remove/?item_id={item_id}&quantity=5")
    assert remove_response.status_code == 200
    assert remove_response.json()["quantity"] == 5

    remove_response = client.post(f"/items/remove/?item_id={item_id}&quantity=5")
    assert remove_response.status_code == 200
    assert remove_response.json()["quantity"] == 0

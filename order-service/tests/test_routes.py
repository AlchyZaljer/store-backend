import pytest


@pytest.mark.usefixtures("override_get_db")
def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Order Service API"}


@pytest.mark.usefixtures("override_get_db")
def test_create_order(client, test_order_data):
    response = client.post("/orders/", json=test_order_data)
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["items"] == test_order_data["items"]
    assert response.json()["discount"] == test_order_data["discount"]


@pytest.mark.usefixtures("override_get_db")
def test_get_order(client, test_order_data):
    create_response = client.post("/orders/", json=test_order_data)
    order_id = create_response.json()["id"]

    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    assert response.json()["id"] == order_id
    assert response.json()["items"] == test_order_data["items"]


@pytest.mark.usefixtures("override_get_db")
def test_list_orders(client, test_order_data):
    client.post("/orders/", json=test_order_data)

    response = client.get("/orders/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["items"] == test_order_data["items"]


@pytest.mark.usefixtures("override_get_db")
def test_update_order(client, test_order_data):
    create_response = client.post("/orders/", json=test_order_data)
    order_id = create_response.json()["id"]

    update_data = {
        "items": [
            {"product_id": 101, "quantity": 5},
            {"product_id": 303, "quantity": 1}
        ],
        "discount": 0.2
    }
    update_response = client.patch(f"/orders/{order_id}", json=update_data)
    assert update_response.status_code == 200
    assert update_response.json()["id"] == order_id
    assert update_response.json()["items"] == update_data["items"]
    assert update_response.json()["discount"] == update_data["discount"]


@pytest.mark.usefixtures("override_get_db")
def test_delete_order(client, test_order_data):
    create_response = client.post("/orders/", json=test_order_data)
    order_id = create_response.json()["id"]

    delete_response = client.delete(f"/orders/{order_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": f"Order {order_id} deleted successfully"}
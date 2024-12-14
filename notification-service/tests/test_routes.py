from datetime import datetime

import pytest


@pytest.mark.usefixtures("override_get_db")
def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Notification Service API"}


@pytest.mark.asyncio
@pytest.mark.usefixtures("override_get_db", "setup_test_data")
async def test_setup_test_data(test_db, test_notification_data):
    count = await test_db.notifications.count_documents({})
    assert count == len(test_notification_data), "Failed to insert test data"


@pytest.mark.usefixtures("override_get_db", "setup_test_data")
def test_get_recent_notifications_single(client):
    response = client.get("/notifications/recent?count=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["message"] == "Fifth test notification"


@pytest.mark.usefixtures("override_get_db", "setup_test_data")
def test_get_recent_notifications_multiple(client):
    response = client.get("/notifications/recent?count=3")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data[0]["message"] == "Fifth test notification"
    assert data[-1]["message"] == "Third test notification"


@pytest.mark.usefixtures("override_get_db", "setup_test_data")
def test_get_notifications_after(client):
    timestamp = "2024-12-14 11:00:00"
    response = client.get(f"/notifications/after?timestamp={timestamp}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data[0]["message"] == "Third test notification"
    assert data[-1]["message"] == "Fifth test notification"

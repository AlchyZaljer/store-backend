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


@pytest.mark.asyncio
@pytest.mark.usefixtures("override_get_db", "setup_test_data")
async def test_get_recent_notifications_single(client, test_db):
    response = client.get("/notifications/recent?count=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    recent_notification = await test_db.notifications.find_one(sort=[("timestamp", -1)])
    assert data[0]["message"] == recent_notification["message"]


@pytest.mark.asyncio
@pytest.mark.usefixtures("override_get_db", "setup_test_data")
async def test_get_recent_notifications_multiple(client, test_db):
    response = client.get("/notifications/recent?count=3")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

    notifications = (
        await test_db.notifications.find(sort=[("timestamp", -1)]).limit(3).to_list(None)
    )
    for i in range(len(data)):
        assert data[i]["message"] == notifications[i]["message"]


@pytest.mark.asyncio
@pytest.mark.usefixtures("override_get_db", "setup_test_data")
async def test_get_notifications_after(client, test_db):
    timestamp = "2024-12-14 11:00:00"
    parsed_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    response = client.get(f"/notifications/after?timestamp={timestamp}")
    assert response.status_code == 200
    data = response.json()

    notifications = await test_db.notifications.find(
        {"timestamp": {"$gt": parsed_time}}
    ).sort("timestamp").to_list(None)

    assert len(data) == len(notifications)
    for i in range(len(data)):
        assert data[i]["message"] == notifications[i]["message"]

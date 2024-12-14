from datetime import datetime

from fastapi.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient
import pytest

from main import app
from database import get_db


@pytest.fixture(scope="function")
def test_db():
    client = AsyncMongoMockClient()
    db = client["test_notification_db"]
    yield db
    client.close()


@pytest.fixture(scope="function")
def override_get_db(test_db):
    async def _override_get_db():
        yield test_db
    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides[get_db] = get_db


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def test_notification_data():
    return [
        {"message": "First test notification", "timestamp": "2024-12-14 10:00:00"},
        {"message": "Second test notification", "timestamp": "2024-12-14 11:00:00"},
        {"message": "Third test notification", "timestamp": "2024-12-14 12:00:00"},
        {"message": "Fourth test notification", "timestamp": "2024-12-14 13:00:00"},
        {"message": "Fifth test notification", "timestamp": "2024-12-14 14:00:00"},
    ]


@pytest.fixture(scope="function")
async def setup_test_data(test_db, test_notification_data):
    for item in test_notification_data:
        item["timestamp"] = datetime.strptime(item["timestamp"], "%Y-%m-%d %H:%M:%S")

    await test_db.notifications.insert_many(test_notification_data)
    yield
    await test_db.notifications.delete_many({})

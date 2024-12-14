from fastapi.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient
import pytest

from main import app
from database import get_db


@pytest.fixture(scope="function")
def test_db():
    client = AsyncMongoMockClient()
    db = client["test_order_db"]
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
def test_order_data():
    return {
        "items": [
            {"product_id": 101, "quantity": 2},
            {"product_id": 202, "quantity": 1}
        ],
        "discount": 0.1
    }

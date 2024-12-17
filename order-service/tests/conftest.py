from fastapi.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient
import pytest
from unittest.mock import AsyncMock, patch

from database import get_db
from main import app


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


@pytest.fixture
def mock_storage_service(mocker):
    with (patch("routes.reserve_products", new=AsyncMock(return_value={"message": "Items reserved successfully"}))
          as mock_reserve,
         patch("routes.return_products", new=AsyncMock(return_value={"message": "Items returned successfully"}))
          as mock_return):
        yield mock_reserve, mock_return

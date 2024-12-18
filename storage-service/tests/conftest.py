from unittest.mock import patch

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import get_db
from main import app
from models import Base


SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def override_get_db(test_db):
    def _override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()
    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides[get_db] = get_db


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def test_item_data():
    return {
        "product_id": 101,
        "quantity": 10
    }


@pytest.fixture
def mock_is_product_exist():
    with patch("utils.is_product_exist", return_value=True):
        yield

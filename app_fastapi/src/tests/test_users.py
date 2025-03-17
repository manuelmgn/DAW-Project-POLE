import pytest
from fastapi.testclient import TestClient
from app_fastapi.src.main import app
from app_fastapi.src.database.database import get_db

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def db():
    db = get_db()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def api_key():
    return ""


import sys
import os
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["REDIS_URL"] = "redis://localhost:6379/0"
os.environ["SECRET_KEY"] = "test-secret"
os.environ["ALGORITHM"] = "HS256"

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db import Base, get_db

import models.user
import models.item
import models.tag
import models.store

from app import create_app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    "sqlite:///./test.db",
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture(autouse=True)
def mock_celery(monkeypatch):
    class MockTask:
        def delay(self, *args, **kwargs):
            return None

    monkeypatch.setattr(
        "routers.auth.send_verification_email",
        MockTask()
    )

@pytest.fixture(scope="function")
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()       
@pytest.fixture(scope="function")
def db_session(setup_db):
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
         

@pytest.fixture(scope="function")
def client(setup_db):
    app = create_app()
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client
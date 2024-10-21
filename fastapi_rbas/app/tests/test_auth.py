import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base
from app.models.user_model import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

# Set up a test database
DATABASE_URL = "postgresql://postgres.foqyncaqywjeijrsnket:ketakidesale@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database and tables
@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(setup_database):
    app.dependency_overrides[get_db] = TestingSessionLocal
    with TestClient(app) as client:
        yield client

def test_register_user(client):
    # Test successful user registration
    response = client.post(
        "/register",
        json={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"

    # Test duplicate user registration
    response = client.post(
        "/register",
        json={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"

def test_login_user(client):
    # First, register a user
    client.post(
        "/register",
        json={"username": "testuser", "password": "testpassword"}
    )

    # Test successful login
    response = client.post(
        "/login",
        data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

    # Test failed login with wrong password
    response = client.post(
        "/login",
        data={"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

    # Test failed login with non-existent user
    response = client.post(
        "/login",
        data={"username": "nonexistentuser", "password": "somepassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

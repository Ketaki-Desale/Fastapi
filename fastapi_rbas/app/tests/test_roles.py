import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base
from app.models.role_model import Role
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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

def test_create_role(client):
    # Test successful role creation
    response = client.post(
        "/roles",
        json={"name": "admin", "permissions": ["create", "read", "update", "delete"]}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "admin"
    assert response.json()["permissions"] == ["create", "read", "update", "delete"]

    # Test duplicate role creation
    response = client.post(
        "/roles",
        json={"name": "admin", "permissions": ["create", "read"]}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Role already exists"

def test_get_roles(client):
    # First, create a role
    client.post(
        "/roles",
        json={"name": "user", "permissions": ["read"]}
    )

    # Test retrieving all roles
    response = client.get("/roles")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    assert any(role["name"] == "admin" for role in response.json())
    assert any(role["name"] == "user" for role in response.json())

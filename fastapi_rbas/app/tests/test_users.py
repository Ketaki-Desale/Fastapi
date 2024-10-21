import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base
from app.models.user_model import User
from app.models.role_model import Role
from app.models.user_role_model import UserRole
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

@pytest.fixture
def create_user(client):
    response = client.post(
        "/register",
        json={"username": "testuser", "password": "testpassword"}
    )
    return response.json()

@pytest.fixture
def create_role(client):
    response = client.post(
        "/roles",
        json={"name": "admin", "permissions": ["create", "read", "update", "delete"]}
    )
    return response.json()

def test_assign_role(client, create_user, create_role):
    user_id = create_user["id"]
    role_id = create_role["id"]

    # Assign role to user
    response = client.post(
        f"/users/{user_id}/roles",
        json={"role_id": role_id}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Role assigned successfully"

    # Verify that the role was assigned
    user_roles_response = client.get(f"/users/{user_id}/roles")
    assert user_roles_response.status_code == 200
    assert any(role["id"] == role_id for role in user_roles_response.json())

def test_remove_role(client, create_user, create_role):
    user_id = create_user["id"]
    role_id = create_role["id"]

    # First, assign the role to the user
    client.post(
        f"/users/{user_id}/roles",
        json={"role_id": role_id}
    )

    # Remove the role from the user
    response = client.delete(
        f"/users/{user_id}/roles/{role_id}"
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Role removed successfully"

    # Verify that the role was removed
    user_roles_response = client.get(f"/users/{user_id}/roles")
    assert user_roles_response.status_code == 200
    assert not any(role["id"] == role_id for role in user_roles_response.json())

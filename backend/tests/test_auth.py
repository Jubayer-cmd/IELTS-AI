"""
Authentication tests.
"""
from fastapi.testclient import TestClient

from app.models import User


def test_register_user(client: TestClient):
    """Test user registration."""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "New User",
            "email": "newuser@example.com",
            "password": "newpass123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["name"] == "New User"
    assert "id" in data


def test_register_duplicate_email(client: TestClient, test_user: User):
    """Test registering with existing email fails."""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Another User",
            "email": test_user.email,
            "password": "somepass123"
        }
    )
    assert response.status_code == 400


def test_login_success(client: TestClient, test_user: User):
    """Test successful login."""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user.email,
            "password": "testpass123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient, test_user: User):
    """Test login with wrong password."""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user.email,
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401


def test_get_current_user(client: TestClient, test_user: User):
    """Test getting current user with token."""
    # First login
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user.email,
            "password": "testpass123"
        }
    )
    token = login_response.json()["access_token"]

    # Then get current user
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user.email

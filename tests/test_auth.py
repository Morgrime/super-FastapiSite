import pytest
from fastapi import status


def test_register_user(client):
    """Test user registration endpoint"""
    response = client.post(
        "/api/auth/register",
        data={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    assert "profile" in data


def test_register_duplicate_username(client, test_user):
    """Test registration with duplicate username"""
    response = client.post(
        "/api/auth/register",
        data={
            "username": "testuser",  # Same as test_user
            "email": "another@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Username already registered" in response.json()["detail"]


def test_login_user(client, test_user):
    """Test user login endpoint"""
    response = client.post(
        "/api/auth/login",
        data={
            "username": "testuser",
            "password": "testpassword"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client, test_user):
    """Test login with invalid credentials"""
    # First ensure the user exists
    response = client.post(
        "/api/auth/register",
        data={
            "username": "invaliduser",
            "email": "invalid@example.com",
            "password": "validpassword"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    
    # Now try to login with wrong password
    response = client.post(
        "/api/auth/login",
        data={
            "username": "invaliduser",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Incorrect password" in response.json()["detail"]


def test_login_nonexistent_user(client):
    """Test login with nonexistent user"""
    response = client.post(
        "/api/auth/login",
        data={
            "username": "nonexistent",
            "password": "password123"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "User does not exist" in response.json()["detail"]


def test_change_password(auth_client, test_user):
    """Test changing password"""
    response = auth_client.post(
        "/api/auth/change_password",
        data={
            "old_password": "testpassword",
            "new_password": "newpassword123"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    
    # Verify we can login with the new password
    response = auth_client.post(
        "/api/auth/login",
        data={
            "username": "testuser",
            "password": "newpassword123"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()


def test_change_password_invalid_old_password(auth_client):
    """Test changing password with invalid old password"""
    response = auth_client.post(
        "/api/auth/change_password",
        data={
            "old_password": "wrongpassword",
            "new_password": "newpassword123"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Invalid old password" in response.json()["detail"] 
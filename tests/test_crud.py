import pytest
from fastapi import status


def test_create_user(client):
    """Test creating a user via CRUD endpoint"""
    response = client.post(
        "/users/",
        json={
            "username": "cruduser",
            "email": "crud@example.com",
            "hashed_password": "hashedpassword123"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == "cruduser"
    assert data["email"] == "crud@example.com"
    assert "id" in data


def test_get_user_by_id(client, test_user):
    """Test getting a user by ID"""
    # First, we need to get the user ID
    # Since we don't have a direct way to get the ID from test_user fixture,
    # we'll create a new user and get its ID
    create_response = client.post(
        "/users/",
        json={
            "username": "getuser",
            "email": "get@example.com",
            "hashed_password": "hashedpassword123"
        }
    )
    user_id = create_response.json()["id"]
    
    # Now get the user by ID
    response = client.get(f"/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == "getuser"
    assert data["email"] == "get@example.com"
    assert data["id"] == user_id


def test_get_user_by_id_not_found(client):
    """Test getting a non-existent user by ID"""
    response = client.get("/users/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "User not found" in response.json()["detail"]


def test_get_all_users(client, test_user):
    """Test getting all users"""
    # Create a few more users to ensure we have multiple users
    client.post(
        "/users/",
        json={
            "username": "user1",
            "email": "user1@example.com",
            "hashed_password": "hashedpassword123"
        }
    )
    client.post(
        "/users/",
        json={
            "username": "user2",
            "email": "user2@example.com",
            "hashed_password": "hashedpassword123"
        }
    )
    
    response = client.get("/users/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3  # At least 3 users (test_user + 2 we just created)


def test_update_user(client):
    """Test updating a user"""
    # First, create a user
    create_response = client.post(
        "/users/",
        json={
            "username": "updateuser",
            "email": "update@example.com",
            "hashed_password": "hashedpassword123"
        }
    )
    user_id = create_response.json()["id"]
    
    # Now update the user
    response = client.put(
        f"/users/{user_id}",
        json={
            "username": "updateduser",
            "email": "updated@example.com"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == "updateduser"
    assert data["email"] == "updated@example.com"
    assert data["id"] == user_id


def test_update_user_not_found(client):
    """Test updating a non-existent user"""
    response = client.put(
        "/users/999",
        json={
            "username": "updateduser",
            "email": "updated@example.com"
        }
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "User not found" in response.json()["detail"]


def test_delete_user(client):
    """Test deleting a user"""
    # First, create a user
    create_response = client.post(
        "/users/",
        json={
            "username": "deleteuser",
            "email": "delete@example.com",
            "hashed_password": "hashedpassword123"
        }
    )
    user_id = create_response.json()["id"]
    
    # Now delete the user
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK
    assert "User deleted successfully" in response.json()["detail"]
    
    # Verify the user is deleted
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_user_not_found(client):
    """Test deleting a non-existent user"""
    response = client.delete("/users/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "User not found" in response.json()["detail"] 
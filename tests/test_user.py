import pytest
from fastapi import status


def test_get_profile(auth_client, test_user):
    """Test getting user profile"""
    response = auth_client.get("/profile")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == test_user["username"]
    assert data["email"] == test_user["email"]
    assert "profile" in data


def test_get_profile_unauthorized(client):
    """Test getting profile without authentication"""
    response = client.get("/profile")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_protected_route(auth_client):
    """Test accessing protected route with authentication"""
    response = auth_client.get("/protected-route")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "message" in data
    assert "user" in data
    assert data["message"] == "This is a protected route"


def test_protected_route_unauthorized(client):
    """Test accessing protected route without authentication"""
    response = client.get("/protected-route")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_test_page(auth_client):
    """Test accessing test page with authentication"""
    response = auth_client.get("/test")
    assert response.status_code == status.HTTP_200_OK
    assert response.text == '"Test page"'


def test_test_page_unauthorized(client):
    """Test accessing test page without authentication"""
    response = client.get("/test")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED 
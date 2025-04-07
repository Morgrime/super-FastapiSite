import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
from typing import AsyncGenerator, Generator

from app.main import app
from app.database.session import get_session
from app.models.base import Base
from app.utils.auth import create_access_token


# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create test session
TestingSessionLocal = sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


# Override the get_session dependency
async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session


# Create test client
@pytest.fixture
def client() -> Generator:
    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


# Setup test database
@pytest.fixture(autouse=True)
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Create test user
@pytest.fixture
async def test_user(client):
    # Register a test user
    response = client.post(
        "/api/auth/register",
        data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword"
        }
    )
    assert response.status_code == 200
    return response.json()


# Create test token
@pytest.fixture
def test_token(test_user):
    access_token = create_access_token(
        data={"sub": test_user["username"]},
        expires_delta=None
    )
    return access_token


# Create authenticated client
@pytest.fixture
def auth_client(client, test_token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {test_token}"
    }
    return client 
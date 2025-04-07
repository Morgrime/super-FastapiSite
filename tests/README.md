# FastAPI Tests

This directory contains tests for the FastAPI application.

## Test Structure

- `conftest.py`: Contains shared test fixtures
- `test_auth.py`: Tests for authentication endpoints
- `test_user.py`: Tests for user profile endpoints
- `test_crud.py`: Tests for CRUD operations

## Running Tests

To run all tests:

```bash
pytest
```

To run a specific test file:

```bash
pytest tests/test_auth.py
```

To run a specific test function:

```bash
pytest tests/test_auth.py::test_login_user
```

To run tests with verbose output:

```bash
pytest -v
```

To run tests with coverage report:

```bash
pytest --cov=app
```

## Test Fixtures

The tests use several fixtures defined in `conftest.py`:

- `client`: A TestClient instance for making HTTP requests
- `auth_client`: A TestClient instance with authentication headers
- `test_user`: A test user created in the database
- `test_token`: A JWT token for the test user

## Test Database

Tests use an in-memory SQLite database to avoid affecting the production database. 
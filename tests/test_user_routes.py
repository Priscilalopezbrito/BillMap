#!/usr/bin/env python3

import pytest
from app import create_app, db

@pytest.fixture
def app():
    """Create a test app instance."""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
    yield app

@pytest.fixture
def client(app):
    """Create a test client for API requests."""
    return app.test_client()

def test_register_user(client):
    """Test user registration route."""
    response = client.post("/users/register", json={
        "name": "John Doe",
        "email": "john@example.com",
        "password": "securepassword"
    })
    assert response.status_code == 201
    assert response.get_json()["message"] == "User registered successfully"

def test_duplicate_email(client):
    """Ensure duplicate emails are not allowed."""
    client.post("/users/register", json={
        "name": "Alice",
        "email": "alice@example.com",
        "password": "password123"
    })
    response = client.post("/users/register", json={
        "name": "Alice2",
        "email": "alice@example.com",
        "password": "password123"
    })
    assert response.status_code == 409  # Conflict

def test_login_user(client):
    """Test user login."""
    client.post("/users/register", json={
        "name": "Bob",
        "email": "bob@example.com",
        "password": "mypassword"
    })
    response = client.post("/users/login", json={
        "email": "bob@example.com",
        "password": "mypassword"
    })
    assert response.status_code == 200
    assert response.get_json()["message"] == "Login successful"

def test_get_user(client):
    """Test getting a user by ID."""
    register_response = client.post("/users/register", json={
        "name": "Charlie",
        "email": "charlie@example.com",
        "password": "testpass"
    })
    user_id = register_response.get_json()["user_id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.get_json()["name"] == "Charlie"

def test_delete_user(client):
    """Test soft deletion of a user."""
    register_response = client.post("/users/register", json={
        "name": "David",
        "email": "david@example.com",
        "password": "pass123"
    })
    user_id = register_response.get_json()["user_id"]

    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.get_json()["message"] == "User deleted successfully"

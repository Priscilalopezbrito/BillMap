#!/usr/bin/env python3

import pytest
from app import create_app, db
from services.user_service import UserService

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
    """Create a test client."""
    return app.test_client()

@pytest.fixture
def init_database(app):
    """Initialize the database before each test."""
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

def test_create_user(init_database):
    """Test user creation."""
    user = UserService.create_user("John Doe", "john@example.com", "securepassword")
    assert user is not None
    assert user.name == "John Doe"
    assert user.email == "john@example.com"

def test_duplicate_email(init_database):
    """Ensure duplicate emails are not allowed."""
    UserService.create_user("John Doe", "john@example.com", "securepassword")
    duplicate = UserService.create_user("Jane Doe", "john@example.com", "securepassword")
    assert duplicate is None  # Should return None since email exists

def test_authenticate_user(init_database):
    """Test user authentication."""
    UserService.create_user("Alice", "alice@example.com", "mypassword")
    user = UserService.authenticate_user("alice@example.com", "mypassword")
    assert user is not None  # Should authenticate successfully
    assert UserService.authenticate_user("alice@example.com", "wrongpassword") is None  # Should fail authentication

def test_delete_user(init_database):
    """Test soft deletion of a user."""
    user = UserService.create_user("Bob", "bob@example.com", "mypassword")
    assert user is not None
    deleted_user = UserService.delete_user(user.id)
    assert deleted_user is not None
    assert deleted_user.deleted_at is not None  # Soft delete should set deleted_at

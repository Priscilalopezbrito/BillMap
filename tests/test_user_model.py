#!/usr/bin/env python3

import pytest
from app import create_app, db
from models.user import User

@pytest.fixture
def app():
    """Create a test app instance."""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # Use an in-memory database
    with app.app_context():
        db.create_all()
    yield app

@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()

@pytest.fixture
def init_database(app):
    """Initialize the database and clear it before and after each test."""
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

def test_create_user(init_database):
    """Test if a user is created successfully."""
    user = User(name="John Doe", email="john@example.com")
    user.set_password("securepassword")  # Hash password
    user.save()  # Save user to DB

    # Query the user back from DB
    saved_user = User.query.filter_by(email="john@example.com").first()
    
    assert saved_user is not None  # Ensure user exists
    assert saved_user.name == "John Doe"
    assert saved_user.email == "john@example.com"
    assert saved_user.password_hash != "securepassword"  # Ensure password is hashed

def test_check_password(init_database):
    """Test password verification."""
    user = User(name="Alice", email="alice@example.com")
    user.set_password("mypassword")
    user.save()

    # Retrieve user from database
    saved_user = User.query.filter_by(email="alice@example.com").first()
    
    assert saved_user is not None
    assert saved_user.check_password("mypassword")  # Correct password
    assert not saved_user.check_password("wrongpassword")  # Incorrect password

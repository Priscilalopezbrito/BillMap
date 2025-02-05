#!/usr/bin/env python3

import pytest
from datetime import date, timedelta
from app import create_app, db
from models.bill import Bill
from models.user import User

@pytest.fixture
def app():
    """Create a test app instance."""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # Use an in-memory database for testing
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

def test_create_bill(init_database):
    """Test if a bill is created successfully."""
    user = User(name="John Doe", email="john@example.com")
    user.set_password("securepassword")
    user.save()

    bill = Bill(
        user_id=user.id,
        amount=100.50,
        due_date=date.today() + timedelta(days=5),  # Due in 5 days
        description="Electricity Bill"
    )
    bill.save()

    # Query the bill from the database
    saved_bill = Bill.query.filter_by(description="Electricity Bill").first()
    
    assert saved_bill is not None  # Ensure the bill exists
    assert saved_bill.user_id == user.id
    assert saved_bill.amount == 100.50
    assert saved_bill.status == "pending"  # Default status

def test_mark_as_paid(init_database):
    """Test if a bill is correctly marked as paid."""
    user = User(name="Alice", email="alice@example.com")
    user.set_password("mypassword")
    user.save()

    bill = Bill(
        user_id=user.id,
        amount=50.00,
        due_date=date.today() + timedelta(days=2),
        description="Water Bill"
    )
    bill.save()

    # Mark as paid
    bill.mark_as_paid()

    # Query the bill again
    updated_bill = Bill.query.filter_by(description="Water Bill").first()
    
    assert updated_bill.status == "paid"

def test_is_overdue(init_database):
    """Test if the is_overdue() method works correctly."""
    user = User(name="Bob", email="bob@example.com")
    user.set_password("securepass")
    user.save()

    overdue_bill = Bill(
        user_id=user.id,
        amount=75.00,
        due_date=date.today() - timedelta(days=3),  # Due 3 days ago
        description="Internet Bill"
    )
    overdue_bill.save()

    # Query the bill again
    saved_bill = Bill.query.filter_by(description="Internet Bill").first()
    
    assert saved_bill.is_overdue() == True  # Should be overdue

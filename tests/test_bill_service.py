#!/usr/bin/env python3

import pytest
from datetime import date, timedelta
from app import create_app, db
from services.bill_service import BillService
from services.user_service import UserService

@pytest.fixture
def app():
    """Create a test app instance."""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # Use in-memory database for testing
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

def test_create_bill(init_database):
    """Test bill creation."""
    user = UserService.create_user("John Doe", "john@example.com", "securepassword")
    bill = BillService.create_bill(user.id, 100.50, date.today() + timedelta(days=5), "Electricity Bill")

    assert bill is not None
    assert bill.user_id == user.id
    assert bill.amount == 100.50
    assert bill.status == "pending"

def test_mark_bill_as_paid(init_database):
    """Test marking a bill as paid."""
    user = UserService.create_user("Alice", "alice@example.com", "mypassword")
    bill = BillService.create_bill(user.id, 75.00, date.today() + timedelta(days=3), "Water Bill")

    BillService.mark_bill_as_paid(bill.id)
    updated_bill = BillService.get_bill_by_id(bill.id)

    assert updated_bill.status == "paid"

def test_check_if_bill_is_overdue(init_database):
    """Test if overdue detection works."""
    user = UserService.create_user("Bob", "bob@example.com", "securepass")
    overdue_bill = BillService.create_bill(user.id, 50.00, date.today() - timedelta(days=3), "Internet Bill")

    assert BillService.check_if_bill_is_overdue(overdue_bill.id) == True

def test_delete_bill(init_database):
    """Test soft deletion of a bill."""
    user = UserService.create_user("Charlie", "charlie@example.com", "testpass")
    bill = BillService.create_bill(user.id, 120.00, date.today() + timedelta(days=10), "Rent Bill")

    deleted_bill = BillService.delete_bill(bill.id)
    assert deleted_bill is not None
    assert deleted_bill.deleted_at is not None  # Ensure soft delete was applied

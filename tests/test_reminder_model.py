#!/usr/bin/env python3

import pytest
from datetime import date, timedelta
from app import create_app, db
from models.reminder import Reminder
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

def test_create_reminder(init_database):
    """Test if a reminder is created successfully."""
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

    reminder = Reminder(
        bill_id=bill.id,
        user_id=user.id,
        reminder_date=date.today(),
        message="Reminder for electricity bill"
    )
    reminder.save()

    # Query the reminder from the database
    saved_reminder = Reminder.query.filter_by(message="Reminder for electricity bill").first()
    
    assert saved_reminder is not None  # Ensure the reminder exists
    assert saved_reminder.user_id == user.id
    assert saved_reminder.bill_id == bill.id
    assert saved_reminder.notification_method == "app_notification"  # Default notification method

def test_is_due(init_database):
    """Test if the is_due() method works correctly."""
    user = User(name="Alice", email="alice@example.com")
    user.set_password("mypassword")
    user.save()

    bill = Bill(
        user_id=user.id,
        amount=50.00,
        due_date=date.today() + timedelta(days=7),
        description="Water Bill"
    )
    bill.save()

    past_reminder = Reminder(
        bill_id=bill.id,
        user_id=user.id,
        reminder_date=date.today() - timedelta(days=3),  # Due 3 days ago
        message="Past reminder for water bill"
    )
    past_reminder.save()

    future_reminder = Reminder(
        bill_id=bill.id,
        user_id=user.id,
        reminder_date=date.today() + timedelta(days=2),  # Due in 2 days
        message="Future reminder for water bill"
    )
    future_reminder.save()

    # Query the reminders again
    saved_past_reminder = Reminder.query.filter_by(message="Past reminder for water bill").first()
    saved_future_reminder = Reminder.query.filter_by(message="Future reminder for water bill").first()
    
    assert saved_past_reminder.is_due() == True  # Past reminder should be due
    assert saved_future_reminder.is_due() == False  # Future reminder should not be due

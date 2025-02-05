#!/usr/bin/env python3

import pytest
from datetime import date, timedelta
from app import create_app, db
from services.reminder_service import ReminderService
from services.bill_service import BillService
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

def test_create_reminder(init_database):
    """Test reminder creation."""
    user = UserService.create_user("John Doe", "john@example.com", "securepassword")
    bill = BillService.create_bill(user.id, 100.50, date.today() + timedelta(days=5), "Electricity Bill")

    reminder = ReminderService.create_reminder(bill.id, user.id, date.today(), "Electricity bill due soon")

    assert reminder is not None
    assert reminder.user_id == user.id
    assert reminder.bill_id == bill.id
    assert reminder.notification_method == "app_notification"

def test_check_if_reminder_is_due(init_database):
    """Test if overdue detection works."""
    user = UserService.create_user("Alice", "alice@example.com", "mypassword")
    bill = BillService.create_bill(user.id, 75.00, date.today() + timedelta(days=3), "Water Bill")

    past_reminder = ReminderService.create_reminder(bill.id, user.id, date.today() - timedelta(days=3), "Water bill reminder")

    assert ReminderService.check_if_reminder_is_due(past_reminder.id) == True

def test_send_notification(init_database):
    """Test if notifications are sent for due reminders."""
    user = UserService.create_user("Bob", "bob@example.com", "securepass")
    bill = BillService.create_bill(user.id, 50.00, date.today() - timedelta(days=3), "Internet Bill")

    due_reminder = ReminderService.create_reminder(bill.id, user.id, date.today() - timedelta(days=2), "Internet bill reminder")
    
    assert ReminderService.send_notification(due_reminder.id) == True

def test_delete_reminder(init_database):
    """Test soft deletion of a reminder."""
    user = UserService.create_user("Charlie", "charlie@example.com", "testpass")
    bill = BillService.create_bill(user.id, 120.00, date.today() + timedelta(days=10), "Rent Bill")

    reminder = ReminderService.create_reminder(bill.id, user.id, date.today(), "Rent reminder")

    deleted_reminder = ReminderService.delete_reminder(reminder.id)
    assert deleted_reminder is not None
    assert deleted_reminder.deleted_at is not None  # Ensure soft delete was applied

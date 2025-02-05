#!/usr/bin/env python3

import pytest
from datetime import date, timedelta
from app import create_app, db

@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_bill(client):
    response = client.post("/bills", json={
        "user_id": 1,
        "amount": 100.50,
        "due_date": (date.today() + timedelta(days=5)).isoformat(),
        "description": "Electricity Bill"
    })
    assert response.status_code == 201
    assert response.get_json()["message"] == "Bill created successfully"

def test_get_bill(client):
    create_response = client.post("/bills", json={
        "user_id": 1,
        "amount": 50.00,
        "due_date": (date.today() + timedelta(days=3)).isoformat(),
        "description": "Water Bill"
    })
    bill_id = create_response.get_json()["bill_id"]

    response = client.get(f"/bills/{bill_id}")
    assert response.status_code == 200
    assert response.get_json()["amount"] == 50.00

def test_update_bill(client):
    create_response = client.post("/bills", json={
        "user_id": 1,
        "amount": 200.00,
        "due_date": (date.today() + timedelta(days=7)).isoformat(),
        "description": "Rent"
    })
    bill_id = create_response.get_json()["bill_id"]

    response = client.put(f"/bills/{bill_id}", json={"amount": 250.00})
    assert response.status_code == 200
    assert response.get_json()["message"] == "Bill updated successfully"

def test_mark_bill_as_paid(client):
    create_response = client.post("/bills", json={
        "user_id": 1,
        "amount": 30.00,
        "due_date": (date.today() + timedelta(days=2)).isoformat(),
        "description": "Phone Bill"
    })
    bill_id = create_response.get_json()["bill_id"]

    response = client.patch(f"/bills/{bill_id}/pay")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Bill marked as paid"

def test_delete_bill(client):
    create_response = client.post("/bills", json={
        "user_id": 1,
        "amount": 75.00,
        "due_date": (date.today() + timedelta(days=10)).isoformat(),
        "description": "Internet Bill"
    })
    bill_id = create_response.get_json()["bill_id"]

    response = client.delete(f"/bills/{bill_id}")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Bill deleted successfully"

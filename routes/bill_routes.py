#!/usr/bin/env python3

from flask import Blueprint, request, jsonify
from services.bill_service import BillService
from datetime import datetime

bill_bp = Blueprint("bill_bp", __name__)

@bill_bp.route("/", methods=["POST"])
def create_bill():
    data = request.get_json()
    user_id = data.get("user_id")
    amount = data.get("amount")
    due_date_str = data.get("due_date")  # Keep as string initially
    description = data.get("description")
    minimum_payment = data.get("minimum_payment")

    if not user_id or not amount or not due_date_str:
        return jsonify({"error": "User ID, amount, and due date are required"}), 400

    try:
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()  # Convert string to date object
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    bill = BillService.create_bill(user_id, amount, due_date, description, minimum_payment)
    return jsonify({"message": "Bill created successfully", "bill_id": bill.id}), 201

@bill_bp.route("/<int:bill_id>", methods=["GET"])
def get_bill(bill_id):
    bill = BillService.get_bill_by_id(bill_id)
    if not bill:
        return jsonify({"error": "Bill not found"}), 404

    return jsonify({
        "id": bill.id,
        "user_id": bill.user_id,
        "amount": bill.amount,
        "due_date": bill.due_date.isoformat(),
        "status": bill.status,
        "description": bill.description,
        "minimum_payment": bill.minimum_payment
    }), 200

@bill_bp.route("/user/<int:user_id>", methods=["GET"])
def get_bills_by_user(user_id):
    bills = BillService.get_bills_by_user(user_id)
    return jsonify([
        {
            "id": bill.id,
            "amount": bill.amount,
            "due_date": bill.due_date.isoformat(),
            "status": bill.status,
            "description": bill.description
        } for bill in bills
    ]), 200

@bill_bp.route("/<int:bill_id>", methods=["PUT"])
def update_bill(bill_id):
    data = request.get_json()
    amount = data.get("amount")
    due_date_str = data.get("due_date")
    description = data.get("description")
    minimum_payment = data.get("minimum_payment")

    due_date = None
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()  # Convert string to date object
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    updated_bill = BillService.update_bill(bill_id, amount, due_date, description, minimum_payment)
    if not updated_bill:
        return jsonify({"error": "Bill not found"}), 404

    return jsonify({"message": "Bill updated successfully"}), 200

@bill_bp.route("/<int:bill_id>/pay", methods=["PATCH"])
def mark_bill_as_paid(bill_id):
    paid_bill = BillService.mark_bill_as_paid(bill_id)
    if not paid_bill:
        return jsonify({"error": "Bill not found"}), 404

    return jsonify({"message": "Bill marked as paid"}), 200

@bill_bp.route("/<int:bill_id>", methods=["DELETE"])
def delete_bill(bill_id):
    deleted_bill = BillService.delete_bill(bill_id)
    if not deleted_bill:
        return jsonify({"error": "Bill not found"}), 404

    return jsonify({"message": "Bill deleted successfully"}), 200

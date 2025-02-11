#!/usr/bin/env python3

from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.bill_service import BillService

# Bill Namespace
api = Namespace("bills", description="Bill/Debt management operations")

# Bill Models for API documentation
bill_model = api.model(
    "Bill",
    {
        "creditor": fields.String(required=True, description="Name of the creditor"),
        "amount": fields.Float(required=True, description="Total amount owed"),
        "due_date": fields.String(required=True, description="Due date (DD/MM/YYYY)"),
        "min_payment": fields.Float(description="Minimum payment required", default=0.0),
        "description": fields.String(description="Optional description"),
    },
)

update_bill_model = api.model(
    "UpdateBill",
    {
        "creditor": fields.String(description="Updated creditor name"),
        "amount": fields.Float(description="Updated total amount owed"),
        "due_date": fields.String(description="Updated due date (DD/MM/YYYY)"),
        "min_payment": fields.Float(description="Updated minimum payment"),
        "description": fields.String(description="Updated description"),
    },
)


def format_bill(bill):
    """Helper function to format bill responses"""
    return {
        "id": str(bill.id),
        "user_id": str(bill.user_id),
        "creditor": bill.creditor,
        "amount": bill.amount,
        "due_date": bill.due_date.strftime("%Y-%m-%d"),
        "min_payment": bill.min_payment,
        "description": bill.description,
        "created_at": bill.created_at.isoformat(),
        "updated_at": bill.updated_at.isoformat(),
        "is_overdue": bill.is_overdue(),
    }


@api.route("/")
class BillList(Resource):
    @jwt_required()
    @api.expect(bill_model, validate=True)
    @api.response(201, "Bill added successfully")
    @api.response(400, "Invalid input data")
    def post(self):
        """Add a new bill for the logged-in user"""
        user_identity = get_jwt_identity()  # Extract JWT payload
        user_id = user_identity["id"]  # Get only the user ID
        
        bill_data = request.get_json()

        try:
            new_bill = BillService.add_debt(
                user_id=user_id,
                creditor=bill_data["creditor"],
                amount=bill_data["amount"],
                due_date=bill_data["due_date"],
                min_payment=bill_data.get("min_payment", 0.0),
                description=bill_data.get("description"),
            )
            return format_bill(new_bill), 201
        except ValueError as e:
            return {"error": str(e)}, 400  # Return proper error response

    @jwt_required()
    @api.response(200, "List of user's bills retrieved successfully")
    def get(self):
        """Retrieve all bills for the logged-in user"""
        user_identity = get_jwt_identity()
        user_id = user_identity["id"]  # Extract only the user ID (string)
        
        bills = BillService.list_all_debts(user_id)
        return [format_bill(bill) for bill in bills], 200


@api.route("/<string:bill_id>")
class BillResource(Resource):
    @jwt_required()
    @api.response(200, "Bill details retrieved successfully")
    @api.response(404, "Bill not found")
    def get(self, bill_id):
        """Get bill details by ID"""
        bill = BillService.get_debt_info(bill_id)
        if not bill:
            return {"error": "Bill not found"}, 404

        return format_bill(bill), 200

    @jwt_required()
    @api.expect(update_bill_model, validate=True)
    @api.response(200, "Bill updated successfully")
    @api.response(403, "Unauthorized action")
    @api.response(404, "Bill not found")
    def put(self, bill_id):
        """Update bill details"""
        user_identity = get_jwt_identity()
        user_id = user_identity["id"]  # Extract only the user ID
        
        bill = BillService.get_debt_info(bill_id)

        if not bill:
            return {"error": "Bill not found"}, 404
        if bill.user_id != user_id:
            return {"error": "Unauthorized action"}, 403

        updated_bill = BillService.update_debt(bill_id, **request.get_json())
        return format_bill(updated_bill), 200

    @jwt_required()
    @api.response(200, "Bill deleted successfully")
    @api.response(403, "Unauthorized action")
    @api.response(404, "Bill not found")
    def delete(self, bill_id):
        """Soft delete a bill"""
        user_identity = get_jwt_identity()
        user_id = user_identity["id"]  # Extract only the user ID
        
        bill = BillService.get_debt_info(bill_id)

        if not bill:
            return {"error": "Bill not found"}, 404
        if bill.user_id != user_id:
            return {"error": "Unauthorized action"}, 403

        BillService.delete_debt(bill_id)
        return {"message": "Bill deleted successfully"}, 200

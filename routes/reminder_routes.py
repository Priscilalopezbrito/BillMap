#!/usr/bin/env python3

from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.reminder_service import ReminderService
from datetime import datetime

# Reminder Namespace
api = Namespace("reminders", description="Reminder management operations")

# Reminder Model for API documentation
reminder_model = api.model(
    "Reminder",
    {
        "bill_id": fields.String(required=True, description="Bill ID associated with the reminder"),
        "reminder_date": fields.String(required=True, description="Reminder date-time (YYYY-MM-DD HH:MM)")
    },
)

update_reminder_model = api.model(
    "UpdateReminder",
    {
        "reminder_date": fields.String(description="Updated reminder date-time (YYYY-MM-DD HH:MM)"),
        "status": fields.String(description="Updated reminder status (pending/sent)")
    },
)


def format_reminder(reminder):
    """Helper function to format reminder responses."""
    return {
        "id": str(reminder.id),
        "user_id": str(reminder.user_id),
        "bill_id": str(reminder.bill_id),
        "reminder_date": reminder.reminder_date.strftime("%Y-%m-%d %H:%M"),
        "status": reminder.status.value,
        "created_at": reminder.created_at.isoformat(),
        "updated_at": reminder.updated_at.isoformat(),
    }

@api.route("/")
class ReminderList(Resource):
    @jwt_required()
    @api.expect(reminder_model, validate=True)
    @api.response(201, "Reminder created successfully")
    def post(self):
        """Create a new reminder for a bill."""
        user_identity = get_jwt_identity()
        user_id = user_identity["id"]
        data = request.get_json()
        
        reminder_datetime = datetime.strptime(data["reminder_date"], "%Y-%m-%d %H:%M")
        new_reminder = ReminderService.create_reminder(user_id, data["bill_id"], reminder_datetime)
        return format_reminder(new_reminder), 201

    @jwt_required()
    @api.response(200, "List of user's reminders retrieved successfully")
    def get(self):
        """Retrieve all reminders for the logged-in user."""
        user_identity = get_jwt_identity()
        user_id = user_identity["id"]
        reminders = ReminderService.get_reminders(user_id)
        return [format_reminder(reminder) for reminder in reminders], 200

@api.route("/<string:reminder_id>")
class ReminderResource(Resource):
    @jwt_required()
    @api.response(200, "Reminder details retrieved successfully")
    @api.response(404, "Reminder not found")
    def get(self, reminder_id):
        """Retrieve a specific reminder."""
        user_identity = get_jwt_identity()
        user_id = user_identity["id"]
        reminder = ReminderService.get_reminders(user_id, reminder_id)
        if not reminder:
            return {"error": "Reminder not found"}, 404
        return format_reminder(reminder), 200

    @jwt_required()
    @api.expect(update_reminder_model, validate=True)
    @api.response(200, "Reminder updated successfully")
    @api.response(404, "Reminder not found")
    def put(self, reminder_id):
        """Update an existing reminder."""
        user_identity = get_jwt_identity()
        user_id = user_identity["id"]
        data = request.get_json()
        
        new_datetime = None
        if "reminder_date" in data:
            new_datetime = datetime.strptime(data["reminder_date"], "%Y-%m-%d %H:%M")
        
        updated_reminder = ReminderService.update_reminder(reminder_id, user_id, new_datetime, data.get("status"))
        if not updated_reminder:
            return {"error": "Reminder not found"}, 404
        return format_reminder(updated_reminder), 200

    @jwt_required()
    @api.response(200, "Reminder deleted successfully")
    @api.response(404, "Reminder not found")
    def delete(self, reminder_id):
        """Soft delete a reminder."""
        user_identity = get_jwt_identity()
        user_id = user_identity["id"]
        deleted_reminder = ReminderService.delete_reminder(reminder_id, user_id)
        if not deleted_reminder:
            return {"error": "Reminder not found"}, 404
        return {"message": "Reminder deleted successfully"}, 200

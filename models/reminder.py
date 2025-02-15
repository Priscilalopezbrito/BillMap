#!/usr/bin/env python3

from models.base_model import BaseModel
from database import db
from datetime import datetime
from enum import Enum

class ReminderStatus(Enum):
    PENDING = "pending"
    SENT = "sent"

class Reminder(BaseModel):
    __tablename__ = "reminders"

    bill_id = db.Column(db.String(36), db.ForeignKey("bills.id"), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    reminder_date = db.Column(db.DateTime, nullable=False)  # Includes date and time
    status = db.Column(db.Enum(ReminderStatus), default=ReminderStatus.PENDING, nullable=False)

    # Relationships
    bill = db.relationship("Bill", backref="reminders", lazy=True)
    user = db.relationship("User", backref="reminders", lazy=True)

    def scheduleReminder(self, reminder_datetime):
        """Sets a reminder for a due date and time."""
        self.reminder_date = reminder_datetime
        self.status = ReminderStatus.PENDING
        self.save()

    def sendReminder(self):
        """Marks the reminder as sent."""
        self.status = ReminderStatus.SENT
        self.save()

    @classmethod
    def getReminder(cls, user_id, reminder_id=None):
        """Fetch details of a specific reminder or all reminders for a user."""
        if reminder_id:
            return cls.query.filter_by(id=reminder_id, user_id=user_id, is_deleted=False).first()
        return cls.query.filter_by(user_id=user_id, is_deleted=False).all()

    def updateStatus(self, new_status):
        """Updates the status of the reminder."""
        if new_status in ReminderStatus.__members__.values():
            self.status = new_status
            self.save()
        else:
            raise ValueError("Invalid status value")

    def deleteReminder(self):
        """Soft deletes the reminder."""
        self.soft_delete()  # Uses BaseModel's soft delete functionality

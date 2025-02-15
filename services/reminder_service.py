#!/usr/bin/env python3

from models.reminder import Reminder, ReminderStatus
from database import db
from datetime import datetime

class ReminderService:
    @staticmethod
    def create_reminder(user_id, bill_id, reminder_datetime):
        """Creates and schedules a new reminder."""
        new_reminder = Reminder(
            user_id=user_id,
            bill_id=bill_id,
            reminder_date=reminder_datetime,
            status=ReminderStatus.PENDING
        )
        new_reminder.save()
        return new_reminder

    @staticmethod
    def get_reminders(user_id, reminder_id=None):
        """Fetches a specific reminder or all reminders for a user."""
        return Reminder.getReminder(user_id, reminder_id)

    @staticmethod
    def update_reminder(reminder_id, user_id, new_datetime=None, new_status=None):
        """Updates an existing reminder's date or status."""
        reminder = Reminder.getReminder(user_id, reminder_id)
        if not reminder:
            return None

        if new_datetime:
            reminder.reminder_date = new_datetime
        if new_status:
            reminder.updateStatus(new_status)
        
        reminder.save()
        return reminder

    @staticmethod
    def delete_reminder(reminder_id, user_id):
        """Soft deletes a reminder."""
        reminder = Reminder.getReminder(user_id, reminder_id)
        if not reminder:
            return None
        
        reminder.deleteReminder()
        return reminder

    @staticmethod
    def send_due_reminders():
        """Sends all due reminders and updates their status."""
        now = datetime.utcnow()
        due_reminders = Reminder.query.filter(
            Reminder.reminder_date <= now,
            Reminder.status == ReminderStatus.PENDING,
            Reminder.is_deleted == False
        ).all()

        for reminder in due_reminders:
            reminder.sendReminder()
        
        db.session.commit()
        return due_reminders

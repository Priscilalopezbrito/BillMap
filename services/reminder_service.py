#!/usr/bin/env python3

from models.reminder import Reminder
from database import db

class ReminderService:
    @staticmethod
    def create_reminder(bill_id, user_id, reminder_date, message=None, notification_method="app_notification"):
        new_reminder = Reminder(
            bill_id=bill_id,
            user_id=user_id,
            reminder_date=reminder_date,
            message=message,
            notification_method=notification_method
        )
        new_reminder.save()
        return new_reminder
    
    @staticmethod
    def get_reminder_by_id(reminder_id):
        return db.session.get(Reminder, reminder_id)
    
    @staticmethod
    def get_reminders_by_user(user_id):
        return Reminder.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def check_if_reminder_is_due(reminder_id):
        reminder = db.session.get(Reminder, reminder_id)
        if not reminder:
            return None
        return reminder.is_due()
    
    @staticmethod
    def send_notification(reminder_id):
        reminder = db.session.get(Reminder, reminder_id)
        if not reminder:
            return None
        
        if reminder.is_due():
            print(f"Sending {reminder.notification_method} reminder: {reminder.message}")
            return True
        return False
    
    @staticmethod
    def update_reminder(reminder_id, reminder_date=None, message=None, notification_method=None):
        reminder = db.session.get(Reminder, reminder_id)
        if not reminder:
            return None
        
        if reminder_date is not None:
            reminder.reminder_date = reminder_date
            
        if message is not None:
            reminder.message = message
        
        if notification_method is not None:
            reminder.notification_method = notification_method
            
        db.session.commit()
        return reminder
    
    @staticmethod
    def delete_reminder(reminder_id):
        reminder = db.session.get(Reminder, reminder_id)
        if not reminder:
            return None
        
        reminder.soft_delete()
        return reminder

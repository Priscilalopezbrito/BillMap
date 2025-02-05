#!/usr/bin/env python3

from models.base_model import BaseModel
from database import db
from datetime import date

class Reminder(BaseModel):
    __tablename__ = 'reminders'
    
    bill_id = db.Column(db.Integer, db.ForeignKey('bills.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reminder_date = db.Column(db.Date, nullable=False)
    notification_method = db.Column(db.String(50), default="app_notification")
    message = db.Column(db.String(255), nullable=True)
    
    def send_notification(self):
        print(f"Sending {self.notification_method} reminder: {self.message}")
        
    def is_due(self):
        return self.reminder_date <= date.today()
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        

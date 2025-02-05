#!/usr/bin/env python3

from models.base_model import BaseModel
from database import db
from datetime import date

class Bill(BaseModel):
    __tablename__ = 'bills'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default="pending")
    minimum_payment = db.Column(db.Float, nullable=True)
    description = db.Column(db.String(255), nullable=True)
    
    def mark_as_paid(self):
        self.status = "paid"
        db.session.commit()
        
    def is_overdue(self):
        return self.due_date < date.today() and self.status != "paid"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        

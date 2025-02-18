#!/usr/bin/env python3

from models.base_model import BaseModel
from database import db
from datetime import datetime
from sqlalchemy.types import TypeDecorator, Date


class DateConverter(TypeDecorator):
    """Custom Date Type that ensures correct format."""
    impl = Date

    def process_bind_param(self, value, dialect):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%d/%m/%Y").date()  # Convert before saving
            except ValueError:
                raise ValueError("Invalid date format. Use DD/MM/YYYY.")
        return value


class Bill(BaseModel):
    __tablename__ = "bills"

    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    creditor = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(DateConverter, nullable=False)  # Use custom converter
    min_payment = db.Column(db.Float, default=0.0)
    description = db.Column(db.Text, nullable=True)

    # Relationships
    user = db.relationship("User", backref="bills", lazy=True)

    def __repr__(self):
        return f"<Bill {self.creditor} - {self.amount} due on {self.due_date}>"

    def update_bill(self, **kwargs):
        """Update bill details"""
        for key, value in kwargs.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)
        self.save()

    def is_overdue(self):
        """Check if the bill is overdue"""
        from datetime import date
        return self.due_date < date.today()

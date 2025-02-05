#!/usr/bin/env python3

from models.bill import Bill
from database import db
from datetime import datetime

class BillService:
    
    @staticmethod
    def create_bill(user_id, amount, due_date, description=None, minimum_payment=None):
        
        if isinstance(due_date, str):
            due_date = datetime.fromisoformat(due_date).date()
            
        new_bill = Bill(
            user_id=user_id,
            amount=amount,
            due_date=due_date,
            description=description,
            minimum_payment=minimum_payment
        )
        new_bill.save()
        return new_bill
    
    @staticmethod
    def get_bill_by_id(bill_id):
        return db.session.get(Bill, bill_id)
    
    @staticmethod
    def get_bills_by_user(user_id):
        return Bill.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def mark_bill_as_paid(bill_id):
        bill = db.session.get(Bill, bill_id)
        if not bill:
            return None
        
        bill.mark_as_paid()
        return bill
    
    @staticmethod
    def check_if_bill_is_overdue(bill_id):
        bill = db.session.get(Bill, bill_id)
        if not bill:
            return None
        
        return bill.is_overdue()
    
    @staticmethod
    def update_bill(bill_id, amount=None, due_date=None, description=None, minimum_payment=None):
        bill = db.session.get(Bill, bill_id)
        if not bill:
            return None
        
        if amount is not None:
            bill.amount = amount
            
        if due_date is not None:
            bill.due_date = due_date
            
        if description is not None:
            bill.description = description
        
        if minimum_payment is not None:
            bill.minimum_payment = minimum_payment
            
        db.session.commit()
        return bill
    
    @staticmethod
    def delete_bill(bill_id):
        bill = db.session.get(Bill, bill_id)
        if not bill:
            return None
        
        bill.soft_delete()
        return bill
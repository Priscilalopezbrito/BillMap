#!/usr/bin/env python3

from models.bill import Bill
from database import db
from datetime import datetime


class BillService:
    
    @staticmethod
    def add_debt(user_id, creditor, amount, due_date, min_payment=0.0, description=None):
        # Validate and convert due_date to a proper date object
        try:
            if isinstance(due_date, str):
                due_date = datetime.strptime(due_date, "%d/%m/%Y").date()  # Convert to date object
        except ValueError:
            raise ValueError("Invalid date format. Please use DD/MM/YYYY.")  # Throw a clear error

        new_bill = Bill(
            user_id=user_id,
            creditor=creditor,
            amount=amount,
            due_date=due_date,  # Now it's a valid date object
            min_payment=min_payment,
            description=description
        )

        new_bill.save()
        return new_bill

    @staticmethod
    def list_all_debts(user_id):
        """Retrieve all debts for a user"""
        return Bill.query.filter_by(user_id=user_id, is_deleted=False).all()

    @staticmethod
    def get_debt_info(debt_id):
        """Get specific debt information"""
        return Bill.query.filter_by(id=debt_id, is_deleted=False).first()

    @staticmethod
    def update_debt(debt_id, **kwargs):
        """Update debt details"""
        debt = BillService.get_debt_info(debt_id)
        if not debt:
            return None

        debt.update_bill(**kwargs)
        return debt

    @staticmethod
    def delete_debt(debt_id):
        """Soft delete a debt (mark as deleted)"""
        debt = BillService.get_debt_info(debt_id)
        if not debt:
            return None
        
        debt.soft_delete()
        return True

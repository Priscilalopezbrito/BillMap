"""
from services.user_service import UserService
from services.bill_service import BillService
from services.reminder_service import ReminderService
"""

"""
class BillMapFacade:

    def __init__(self):
        self.user_service = UserService()
        self.bill_service = BillService()
        self.reminder_service = ReminderService()

    # ---- User Management ----
    def register_user(self, name, email, password):
        
        return self.user_service.create_user(name, email, password)

    def login_user(self, email, password):
        
        return self.user_service.authenticate_user(email, password)

    # ---- Bill Management ----
    def add_bill(self, user_id, amount, due_date):
        
        return self.bill_service.add_bill(user_id, amount, due_date)

    def get_user_bills(self, user_id):
        
        return self.bill_service.get_bills(user_id)

    # ---- Reminder Management ----
    def add_reminder(self, user_id, bill_id, reminder_date):
        
        return self.reminder_service.add_reminder(user_id, bill_id, reminder_date)

    def get_user_reminders(self, user_id):
        
        return self.reminder_service.get_reminders(user_id)
"""
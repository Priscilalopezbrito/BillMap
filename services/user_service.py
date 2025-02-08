from models.user import User
from database import db


class UserService:

    @staticmethod
    def create_user(first_name, last_name, email, password):
        if User.query.filter_by(email=email).first():
            return None

        new_user = User(first_name=first_name, last_name=last_name, email=email)
        new_user.set_password(password)
        new_user.save()

        return new_user

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.filter_by(id=user_id).first()

    @staticmethod
    def get_user_by_email(email):
        return User.get_active().filter_by(email=email).first()

    @staticmethod
    def authenticate_user(email, password):
        """Authenticate a user by email and password"""
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            return user
        return None

    @staticmethod
    def update_user(user_id, **kwargs):
        """Update user details"""
        user = UserService.get_user_by_id(user_id)
        if not user:
            return None

        for key, value in kwargs.items():
            if hasattr(user, key) and value:
                setattr(user, key, value)

        db.session.commit()
        return user

    @staticmethod
    def delete_user(user_id):
        """Permanently delete a user"""
        user = UserService.get_user_by_id(user_id)
        if not user:
            return None

        db.session.delete(user)
        db.session.commit()
        return True

    @staticmethod
    def get_all_users():

        return User.query.all()

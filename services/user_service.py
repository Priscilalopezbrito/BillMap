#!/usr/bin/env python3

from models.user import User
from database import db

class UserService:
    
    @staticmethod
    def create_user(name, email, password):
        if User.query.filter_by(email=email).first():
            return None
        
        new_user = User(name=name, email=email)
        new_user.set_password(password)
        new_user.save()
        
        return new_user
    
    @staticmethod
    def get_user_by_id(user_id):
        return db.session.get(User, user_id)
    
    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def authenticate_user(email, password):
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return user
        return None
    
    @staticmethod
    def update_user(user_id, name=None, email=None):
        user = db.session.get(User, user_id)
        if not user:
            return None
        
        if name:
            user.name = name
        if email and not User.query.filter_by(email=email).first():
            user.email = email
            
        db.session.commit()
        return user
    
    @staticmethod
    def delete_user(user_id):
        user = db.session.get(User, user_id)
        if not user:
            return None
        
        user.soft_delete()
        return user
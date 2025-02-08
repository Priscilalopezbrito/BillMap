#!/usr/bin/env python3

from models.base_model import BaseModel
from database import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


class User(BaseModel):
    __tablename__ = "users"

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        """Hash and store password"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Verify provided password against stored hash"""
        return bcrypt.check_password_hash(self.password_hash, password)

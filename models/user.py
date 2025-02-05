#!/usr/bin/env python3

from werkzeug.security import generate_password_hash, check_password_hash
from models.base_model import BaseModel
from database import db

class User(BaseModel):
    __tablename__ = "users"
    
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120),unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

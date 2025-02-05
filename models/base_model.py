#!/usr/bin/env python3

from datetime import datetime
from database import db


class BaseModel(db.Model):
    __abstract__ = True 
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True) 
    
    def soft_delete(self):
        self.deleted_at = datetime.utcnow()
        db.session.commit()

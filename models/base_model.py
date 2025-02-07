#!/usr/bin/env python3

import uuid
from datetime import datetime
from database import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)

    def save(self):
        """Save the object to the database"""
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """Update the attributes of the object and save"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Save changes

    def soft_delete(self):
        """Soft delete object instead of removing it permanently"""
        self.is_deleted = True
        self.save()

    @classmethod
    def get_active(cls):
        """Retrieve only active records"""
        return cls.query.filter_by(is_deleted=False)

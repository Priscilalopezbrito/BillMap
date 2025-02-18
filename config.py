#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_jwt_secret_key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=50)  # Customize auth token to last 50 minutes
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///billmap.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv("DEBUG", "False").strip().lower() in ["1", "true", "yes"]

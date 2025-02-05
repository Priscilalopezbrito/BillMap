#!/usr/bin/env python3

from flask import Flask, jsonify
from database import db
from flask_cors import CORS
from config import Config
from models.user import User
from models.bill import Bill
from models.reminder import Reminder

from routes.user_routes import user_bp
from routes.bill_routes import bill_bp

#from routes.reminder_routes import reminder_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    
    db.init_app(app)
    
    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(bill_bp, url_prefix="/bills")
    #app.register_blueprint(reminder_bp, url_prefix="/reminders")
    
    
    @app.route("/health", methods=["GET"])
    def health_check():
        return jsonify({"status": "ok"}), 200
    
    return app

if __name__ == "__main__":
    app = create_app()
    
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)

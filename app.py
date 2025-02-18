#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restx import Api

from config import Config
from database import db
from routes.user_routes import api as user_ns
from routes.bill_routes import api as bill_ns
from routes.reminder_routes import api as reminder_ns
from routes.auth import api as auth_ns

# Initialize Flask extensions
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app():
    """Initialize Flask application and extensions"""
    app = Flask(__name__)

    # Load Configuration
    app.config.from_object(Config)

    # Initialize Extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # Bearer Authentication for Swagger
    authorizations = {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "bearerFormat": "JWT",
        }
    }

    # Initialize API with Authentication in Swagger
    api = Api(
        app,
        version="1.0",
        title="BillMAP API",
        description="BillMAP Application API",
        authorizations=authorizations,
        security="BearerAuth",
        doc="/"  # Swagger available at root
    )

    # Namespaces
    api.add_namespace(user_ns, path="/api/v1/users")
    api.add_namespace(auth_ns, path="/api/v1/auth")
    api.add_namespace(bill_ns, path="/api/v1/bills")
    api.add_namespace(reminder_ns, path="/api/v1/reminder")

    @app.route("/", methods=["GET"])
    def home():
        """Home page"""
        return jsonify({"message": "Welcome to BillMap API! Use /api/v1/users or /api/v1/bills"}), 200

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Database tables checked/created successfully!")

    app.run(debug=Config.DEBUG, port=5001)

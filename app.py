#!/usr/bin/env python3
from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from database import db
from config import Config
from flask_bcrypt import Bcrypt

from routes.user_routes import api as user_ns
#  from routes.bill_routes import api as bill_ns
#  from routes.reminder_routes import api as reminder_ns

from flask_restx import Api

bcrypt = Bcrypt()


def create_app():
    """Initialize Flask application"""
    app = Flask(__name__)

    # Load Configuration
    app.config.from_object(Config)
    CORS(app)

    #  Initialize Database & Migrations
    db.init_app(app)
    bcrypt.init_app(app)
    Migrate(app, db)

    #  Bearer Authentication for Swagger
    authorizations = {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
        }
    }

    #  Initialize API with Authentication in Swagger
    api = Api(
        app,
        version="1.0",
        title="BillMAP API",
        description="BillMAP Application API",
        authorizations=authorizations,
        security="BearerAuth",
        doc="/"  # Swagger available at /
    )

    #  Namespaces
    api.add_namespace(user_ns, path="/api/v1/users")
    #  api.add_namespace(bill_ns, path="/api/v1/bills")

    @app.route("/", methods=["GET"])
    def home():
        """Homepage"""
        return jsonify({"message": "Welcome to BillMap API! Use /api/v1/users or /api/v1/bills"}), 200

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Database tables checked/created successfully!")
    app.run(debug=True, port=5001)

from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from services.plaid_service import PlaidService
from datetime import date, datetime
import json

api = Namespace("Plaid", description="Plaid API Integration")

plaid_service = PlaidService()


# Helper function to handle JSON serialization issues
def json_serial(obj):
    """Convert non-serializable types to JSON serializable formats."""
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()  # Convert dates to string format
    raise TypeError(f"Type {type(obj)} not serializable")


# Define request models
exchange_token_model = api.model(
    "ExchangeToken", {"public_token": fields.String(required=True, description="Public token from Plaid Link")}
)

transactions_request_model = api.model(
    "GetTransactions",
    {
        "access_token": fields.String(required=True, description="Plaid access token"),
        "start_date": fields.String(required=True, description="Start date (YYYY-MM-DD)"),
        "end_date": fields.String(required=True, description="End date (YYYY-MM-DD)"),
    },
)


@api.route("/create_link_token")
class CreateLinkToken(Resource):
    def get(self):
        """Generate a Link Token for Plaid Link"""
        try:
            response = plaid_service.create_link_token(user_id="user123")

            if isinstance(response, dict):
                return response  # Flask-RESTX will handle JSON serialization
            else:
                return {"error": "Unexpected response format"}, 500
        except Exception as e:
            return {"error": str(e)}, 500


@api.route("/exchange_token")
class ExchangeToken(Resource):
    @api.expect(exchange_token_model)
    def post(self):
        """Exchange public token for access token"""
        try:
            data = request.json
            if "public_token" not in data:
                return {"error": "Missing public_token"}, 400

            response = plaid_service.exchange_public_token(data["public_token"])
            if "error" in response:
                return response, 400  # Return as JSON with HTTP 400
            return response
        except Exception as e:
            return {"error": str(e)}, 500


@api.route("/liabilities")
class GetLiabilities(Resource):
    def get(self):
        """Retrieve liabilities from Plaid"""
        try:
            access_token = request.args.get("access_token")
            print(f"🔍 DEBUG - Received Access Token: {access_token}")

            if not access_token:
                return {"error": "Missing access_token"}, 400

            response = plaid_service.get_liabilities(access_token)
            print(f"🔍 DEBUG - Liabilities Response: {response}")

            #  FIX: Ensure JSON serialization
            return json.loads(json.dumps(response, default=json_serial))

        except Exception as e:
            print(f" ERROR - Unexpected: {str(e)}")
            return {"error": str(e)}, 500


@api.route("/transactions")
class GetTransactions(Resource):
    @api.expect(transactions_request_model)
    def post(self):
        """Retrieve transactions from Plaid"""
        try:
            data = request.json
            if not all(k in data for k in ["access_token", "start_date", "end_date"]):
                return {"error": "Missing required fields"}, 400

            response = plaid_service.get_transactions(
                data["access_token"], data["start_date"], data["end_date"]
            )

            if "error" in response:
                return response, 400

            #  FIX: Ensure JSON serialization
            return json.loads(json.dumps({"transactions": response}, default=json_serial))

        except Exception as e:
            return {"error": str(e)}, 500

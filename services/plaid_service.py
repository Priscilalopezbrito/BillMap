import os
import json
import time
import datetime
from datetime import datetime, date
from dotenv import load_dotenv
from plaid import ApiException
from plaid.api import plaid_api
from plaid.model.liabilities_get_request import LiabilitiesGetRequest
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.configuration import Configuration
from plaid.api_client import ApiClient
from plaid.model.country_code import CountryCode
from plaid.model.products import Products
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser

# Load environment variables
load_dotenv()


class PlaidService:
    def __init__(self):
        self.client_id = os.getenv("PLAID_CLIENT_ID")
        self.secret = os.getenv("PLAID_SECRET")
        self.env = os.getenv("PLAID_ENV", "sandbox")

        # ✅ Ensure API keys are set
        if not self.client_id or not self.secret:
            raise ValueError("PLAID_CLIENT_ID and PLAID_SECRET must be set in environment variables.")

        configuration = Configuration(
            host=self._get_environment(),
            api_key={
                "clientId": self.client_id,
                "secret": self.secret,
                "plaidVersion": "2020-09-14",
            },
        )
        api_client = ApiClient(configuration)
        self.client = plaid_api.PlaidApi(api_client)

    def _get_environment(self):
        """Retrieve the correct Plaid environment."""
        from plaid import Environment

        env_mapping = {
            "sandbox": Environment.Sandbox,
            "production": Environment.Production
        }
        return env_mapping.get(self.env.lower(), Environment.Sandbox)

    def create_link_token(self, user_id):
        """Generate a Plaid Link Token"""
        try:
            request = LinkTokenCreateRequest(
                user=LinkTokenCreateRequestUser(client_user_id=str(user_id)),
                client_name="Your App",
                products=[Products("transactions"), Products("liabilities")],
                country_codes=[CountryCode("US")],
                language="en"
            )

            response = self.client.link_token_create(request).to_dict()

            #  Convert datetime objects to strings
            def convert_datetime(obj):
                if isinstance(obj, datetime):
                    return obj.isoformat()  # Convert to string format
                raise TypeError(f"Type {type(obj)} not serializable")

            return json.loads(json.dumps(response, default=convert_datetime))  # Ensure JSON-serializable output

        except ApiException as e:
            return {"error": json.loads(e.body)}

    def exchange_public_token(self, public_token):
        """Exchange public token for access token."""
        try:
            request = ItemPublicTokenExchangeRequest(public_token=public_token)
            response = self.client.item_public_token_exchange(request).to_dict()

            # ✅ Print access token for debugging
            print("🔑 DEBUG - Access Token:", response["access_token"])

            return response  # Ensure this is returned correctly
        except ApiException as e:
            return {"error": json.loads(e.body)}

    def get_liabilities(self, access_token):
        """Retrieve liabilities (credit, student loans, mortgages)."""
        try:
            request = LiabilitiesGetRequest(access_token=access_token)
            response = self.client.liabilities_get(request)

            # Convert response to a dictionary
            liabilities_data = response.to_dict()

            return liabilities_data
        except ApiException as e:
            return {"error": json.loads(e.body)}

    def get_transactions(self, access_token, start_date, end_date):
        """Retrieve transaction history."""
        try:
            cursor = ''
            transactions = []
            has_more = True

            while has_more:
                request = TransactionsSyncRequest(
                    access_token=access_token, cursor=cursor
                )
                response = self.client.transactions_sync(request).to_dict()
                transactions.extend(response["added"])
                cursor = response["next_cursor"]
                has_more = response["has_more"]
                time.sleep(1)

            return {"transactions": transactions}  # ✅ Ensures JSON-serializable output
        except ApiException as e:
            return {"error": json.loads(e.body)}

#!/usr/bin/env python3

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from services.user_service import UserService

api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})


@api.route('/login')
class Login(Resource):
    @api.expect(login_model, validate=True)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload

        # Step 1: Retrieve the user based on the provided email
        user = UserService.get_user_by_email(credentials['email'])
        if not user or not user.check_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # Step 2: Create a JWT token with user details (Fix)
        access_token = create_access_token(identity={"id": str(user.id), "email": user.email})

        # Step 3: Return the JWT token to the client
        return {'access_token': access_token}, 200


@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """Protected route example"""
        current_user = get_jwt_identity()
        return {'message': f'Hello, user {current_user}'}, 200

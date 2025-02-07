#!/usr/bin/env python3

from flask import request
from flask_restx import Namespace, Resource, fields
from services.user_service import UserService  # UserService logic (facade)

# User Namespace
api = Namespace('users', description='User operations')

# User Models
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email'),
    'password': fields.String(required=True, description='Password')
})

update_user_model = api.model('UpdateUser', {
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'email': fields.String(description='New email')
})


def format_user(user):
    """Helper function to format user responses"""
    return {
        "id": str(user.id),
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email
    }


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    def post(self):
        """Create new user"""
        user_data = request.get_json()
        if UserService.get_user_by_email(user_data['email']):
            return {"error": "Email already registered"}, 400

        new_user = UserService.create_user(
            user_data['first_name'], user_data['last_name'],
            user_data['email'], user_data['password']
        )
        return format_user(new_user), 201


@api.route('/<string:user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user by ID"""
        user = UserService.get_user_by_id(user_id)

        if not user:
            return {"error": "User not found"}, 404

        return format_user(user), 200


@api.route('/user-list')
class Users(Resource):
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Get all users"""
        users = UserService.get_all_users()
        return [format_user(user) for user in users], 200


@api.route('/update/<string:user_id>')
class UpdateUser(Resource):
    @api.expect(update_user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Email already in use')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user information"""
        user_data = request.get_json()

        # Check if email is already in use, if not update
        if 'email' in user_data and UserService.get_user_by_email(user_data['email']):
            return {"error": "Email already in use"}, 400

        updated_user = UserService.update_user(user_id, **user_data)
        if not updated_user:
            return {"error": "User not found"}, 404

        return format_user(updated_user), 200


@api.route('/delete/<string:user_id>')
class DeleteUser(Resource):
    @api.response(200, 'User deleted successfully')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """Soft delete a user"""
        if UserService.delete_user(user_id):
            return {"message": "User deleted successfully"}, 200
        return {"error": "User not found"}, 404

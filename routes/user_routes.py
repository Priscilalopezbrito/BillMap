#!/usr/bin/env python3

from flask import Blueprint, request, jsonify
from services.user_service import UserService

user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    user = UserService.create_user(name, email, password)
    if user is None:
        return jsonify({"error": "Email already exists"}), 409  # Conflict

    return jsonify({"message": "User registered successfully", "user_id": user.id}), 201

@user_bp.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = UserService.authenticate_user(email, password)
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401  # Unauthorized

    return jsonify({"message": "Login successful", "user_id": user.id}), 200

@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = UserService.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"id": user.id, "name": user.name, "email": user.email}), 200

@user_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    updated_user = UserService.update_user(user_id, name, email)
    if not updated_user:
        return jsonify({"error": "User not found or email already in use"}), 404

    return jsonify({"message": "User updated successfully"}), 200

@user_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    deleted_user = UserService.delete_user(user_id)
    if not deleted_user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "User deleted successfully"}), 200

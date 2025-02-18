#!/usr/bin/python3
"""
Users API routes.
Handles all default RESTful API actions for User objects.
"""

from flask import jsonify, request, abort
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects."""
    return jsonify([user.to_dict() for user in storage.all(User).values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a specific User object by ID."""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object by ID."""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a new User object."""
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data = request.get_json()
    if "email" not in data:
        return jsonify({"error": "Missing email"}), 400
    if "password" not in data:
        return jsonify({"error": "Missing password"}), 400

    new_user = User(**data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates an existing User object."""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data = request.get_json()
    ignored_keys = ["id", "email", "created_at", "updated_at"]

    for key, value in data.items():
        if key not in ignored_keys:
            setattr(user, key, value)

    user.save()
    return jsonify(user.to_dict()), 200

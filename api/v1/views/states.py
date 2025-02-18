#!/usr/bin/python3
"""
States API routes.
Handles all default RESTful API actions for State objects.
"""

from flask import jsonify, request, abort
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects."""
    return jsonify([state.to_dict() for state in storage.all(State).values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a specific State object by ID."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object by ID."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a new State object."""
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data = request.get_json()
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400

    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates an existing State object."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data = request.get_json()
    ignored_keys = ["id", "created_at", "updated_at"]

    for key, value in data.items():
        if key not in ignored_keys:
            setattr(state, key, value)

    state.save()
    return jsonify(state.to_dict()), 200

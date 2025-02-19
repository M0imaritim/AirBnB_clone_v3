#!/usr/bin/python3
"""
Amenities API routes.
Handles all default RESTful API actions for Amenity objects.
"""

from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects."""
    return jsonify([amenity.to_dict()
                    for amenity in storage.all(Amenity).values()])


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a specific Amenity object by ID."""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an Amenity object by ID."""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities',
                 methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a new Amenity object."""
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data = request.get_json()
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400

    new_amenity = Amenity(**data)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an existing Amenity object."""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data = request.get_json()
    ignored_keys = ["id", "created_at", "updated_at"]

    for key, value in data.items():
        if key not in ignored_keys:
            setattr(amenity, key, value)

    amenity.save()
    return jsonify(amenity.to_dict()), 200

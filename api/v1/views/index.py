#!/usr/bin/python3
"""
Index route for the API v1
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns the API status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """Endpoint to retrieve the number of each object by type"""
    # Call the count method from storage
    object_counts = storage.count()
    # Return the count as a JSON response
    return jsonify(object_counts)

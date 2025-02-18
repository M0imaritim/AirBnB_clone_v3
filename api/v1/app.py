#!/usr/bin/python3
"""
Flask application setup for the HBNB API
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os

# Create a Flask instance
app = Flask(__name__)

# Register the blueprint
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Close the storage session after each request"""
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    """Handler for 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    # Get host and port from environment variables or use defaults
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))

    # Run the Flask app
    app.run(host=host, port=port, threaded=True)

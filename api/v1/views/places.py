#!/usr/bin/python3
"""Handles searching for Place objects based on request filters"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from werkzeug.exceptions import BadRequest  # To handle invalid JSON


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    POST /api/v1/places_search
    Retrieves all Place objects based on JSON body filters.
    ---
    JSON body can contain:
      - "states": list of State ids
      - "cities": list of City ids
      - "amenities": list of Amenity ids
    """

    # Parse JSON body safely
    try:
        data = request.get_json()
        if not isinstance(data, dict):  # Ensure it's a valid JSON object
            abort(400, description="Not a JSON")
    except BadRequest:
        abort(400, description="Not a JSON")

    # Extract filters from request body
    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    # Retrieve all places if no filters are applied
    if not states and not cities and not amenities:
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    place_set = set()

    # Fetch places from states (including all their cities)
    if states:
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    place_set.update(city.places)

    # Fetch places from cities
    if cities:
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                place_set.update(city.places)

    # Convert set to list for further filtering
    places = list(place_set)

    # If amenities are provided, filter places to only those with all amenities
    if amenities:
        filtered_places = []
        for place in places:
            place_amenities = {a.id for a in place.amenities}
            if all(amenity_id in place_amenities for amenity_id in amenities):
                filtered_places.append(place)
        places = filtered_places

    return jsonify([place.to_dict() for place in places])

#!/usr/bin/python3
"""Places API endpoint"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from werkzeug.exceptions import BadRequest


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    POST /api/v1/places_search
    Searches for Place objects based on JSON body.
    """
    # Ensure request body is valid JSON
    try:
        data = request.get_json()
        if data is None:  # get_json() returns None if content is not JSON
            abort(400, description="Not a JSON")
    except BadRequest:
        abort(400, description="Not a JSON")

    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    # Retrieve all places if no filters are applied
    if not states and not cities and not amenities:
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    place_set = set()

    # If states are provided, fetch all places in each state's cities
    if states:
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    place_set.update(city.places)

    # If cities are provided, fetch places from each city
    if cities:
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                place_set.update(city.places)

    # Convert set to list for further filtering
    places = list(place_set)

    # If amenities are provided, filter places to include
    # only those with all amenities
    if amenities:
        filtered_places = []
        for place in places:
            if all(amenity_id in [a.id for a in place.amenities]
                   for amenity_id in amenities):
                filtered_places.append(place)
        places = filtered_places

    return jsonify([place.to_dict() for place in places])

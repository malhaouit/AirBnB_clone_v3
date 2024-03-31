#!/usr/bin/python3
"""Place view for API v1."""
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views


@app_views.route(
        '/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
        '/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    if 'user_id' not in request.json:
        abort(400, description="Missing user_id")
    user_id = request.json['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if 'name' not in request.json:
        abort(400, description="Missing name")
    place = Place(city_id=city_id, **request.get_json())
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in request.get_json().items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route(
        '/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Retrieves all Place objects depending of the JSON in the body of the
    request."""
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")

    # Initialize filters
    states_ids = body.get('states', [])
    cities_ids = body.get('cities', [])
    amenities_ids = body.get('amenities', [])

    # Collect all places if no specific filters are applied
    if not body or (not states_ids and not cities_ids and not amenities_ids):
        places = storage.all(Place).values()
    else:
        places = []
        # Add places based on state IDs
        if states_ids:
            for state_id in states_ids:
                state = storage.get("State", state_id)
                if state:
                    for city in state.cities:
                        places.extend(city.places)
        # Add places based on city IDs
        if cities_ids:
            for city_id in cities_ids:
                city = storage.get("City", city_id)
                if city and city not in [place.city for place in places]:
                    places.extend(city.places)

        # Filter places by amenities
        def is_place_valid(place, amenities_ids):
            """
            Check if a place has all amenities specified by amenities_ids
            """
            return all(
                    amenity.id in amenities_ids for amenity in place.amenities
                    )

        if amenities_ids:
            places = [
                    place for place in places if is_place_valid(
                        place, amenities_ids
                        )
                    ]

    # Serialize and return the filtered places
    places_list = [place.to_dict() for place in places]
    return jsonify(places_list)

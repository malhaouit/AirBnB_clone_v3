#!/usr/bin/python3
"""Reviews view for API v1."""
from flask import abort, jsonify, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views


@app_views.route(
        '/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """Retrieves the list of all Review objects of a Place."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object."""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
        '/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Creates a Review."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    if 'user_id' not in request.json:
        abort(400, description="Missing user_id")
    user_id = request.json['user_id']
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if 'text' not in request.json:
        abort(400, description="Missing text")
    review_data = request.get_json()
    review_data['place_id'] = place_id
    review = Review(**review_data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object."""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in request.get_json().items():
        if key not in ignore_keys:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200


@app_views.route(
        '/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object."""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200

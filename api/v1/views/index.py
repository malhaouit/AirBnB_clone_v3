#!/usr/bin/python3
"""Index module for the API v1 views."""

from flask import jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage

classes = {
    "amenities": Amenity,
    "cities": City,
    "places": Place,
    "reviews": Review,
    "states": State,
    "users": User
}


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return a JSON with 'status': 'OK'."""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def count_stats():
    """Retrieves the number of each object by type."""
    counts = {
            cls_name: storage.count(cls) for cls_name, cls in classes.items()
            }
    return jsonify(counts)

#!/usr/bin/python3
"""Index module for the API v1 views."""

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return a JSON with 'status': 'OK'."""
    return jsonify({"status": "OK"})

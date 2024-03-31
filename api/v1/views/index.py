#!/usr/bin/pyhton3
"""Defines /status route"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Defines /status route on the object app_views that returns a JSON:
        'status': 'OK'"""
    return jsonify({"status": "OK"})

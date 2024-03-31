#!/usr/bin/python3
"""Flask app"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
from os import getenv

app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """Handler for 404 errors that returns a JSON-formatted 404 response."""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def close_storage(exception):
    """Closes the storage"""
    storage.close()


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)

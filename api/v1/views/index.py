#!/usr/bin/python3
""" Flask route that returns the Json status"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)  # , methods=['GET'])
def status():
    """ Returns the Status of your API"""
    my_status = {"status": "OK"}
    return jsonify(my_status)


@app_views.route('/stats', strict_slashes=False)
def stats():
    """ retrieves the number of each objects by type """
    clases = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
    }
    json_response = {}
    for key, value in clases.items():
        val = storage.count(value)
        json_response[key] = val
    return jsonify(json_response)

#!/usr/bin/python3
""" This file contain the reponse of API status
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


@app_views.route('/status', strict_slashes=False)
def response():
    """JSON responde of API status"""
    return jsonify({'status': 'ok' })


@app_views.route('/stats', strict_slashes=False)
def counter():
    """Funtion that return the number of objects by class"""
    return jsonify({"amenities": storage.count(classes["Amenity"]),
                   "cities": storage.count(classes["City"]),
                   "places": storage.count(classes["Place"]),
                   "reviews": storage.count(classes["Review"]),
                   "states": storage.count(classes["State"]),
                   "users": storage.count(classes["User"])})

if __name__ == "__main__":
    pass

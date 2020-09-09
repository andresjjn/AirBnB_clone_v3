#!/usr/bin/python3
""" New view for City objects that handles all default RestFul API actions:"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def all_amenities():
    """Retrieves the list of all Amenity objects"""
    dict_amenities = []
    for amenity_obj in storage.all("Amenity").values():
        dict_amenities.append(amenity_obj.to_dict())
    return jsonify(dict_amenities)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['GET'])
def amenity_id(amenity_id):
    """ Retrieves a Amenity object based on the amenity_id """
    dict_amenity = storage.get("Amenity", amenity_id)
    if dict_amenity is None:
        abort(404)
    return jsonify(dict_amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def amenity_deletes(amenity_id):
    """Deletes an object Amenity"""
    obj_amenity = storage.get("Amenity", amenity_id)
    if obj_amenity is None:
        abort(404)
    storage.delete(obj_amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def anenity_post():
    """ transform the HTTP body request to a dictionary"""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        abort(400, description="Not a JSON")
    if "name" not in data.keys():
        abort(400, description="Missing name")
    obj_amenity = Amenity(**data)
    storage.new(obj_amenity)
    storage.save()
    return jsonify(obj_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def amenity_put(amenity_id):
    """Updates an Amenity object using amenity_id"""
    obj_amenity = storage.get("Amenity", amenity_id)
    if obj_amenity is None:
        abort(404)
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key != "id" and key != "created_at" and key != "updated_at":
            setattr(obj_amenity, key, value)
    obj_amenity.save()
    return jsonify(obj_amenity.to_dict()), 200

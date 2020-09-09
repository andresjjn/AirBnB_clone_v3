#!/usr/bin/python3
""" New view for City objects that handles all default RestFul API actions:"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def all_cities(state_id):
    """Retrieves the list of all City objects"""
    dict_cities = []
    dict_state = storage.get("State", state_id)
    if dict_state is None:
        abort(404)
    for city in dict_state.cities:
        dict_cities.append(city.to_dict())
    return jsonify(dict_cities)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def city_id(city_id):
    """ Retrieves a City object based on the city_id """
    dict_city = storage.get("City", city_id)
    if dict_city is None:
        abort(404)
    return jsonify(dict_city.to_dict())


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def city_deletes(city_id):
    """Deletes an object City"""
    obj_city = storage.get("City", city_id)
    if obj_city is None:
        abort(404)
    storage.delete(obj_city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def city_post(state_id):
    """ Transform the HTTP body request to a dictionary"""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        abort(400, description="Not a JSON")
    if "name" not in data.keys():
        abort(400, description="Missing name")
    data['state_id'] = state_id
    obj_city = City(**data)
    storage.new(obj_city)
    storage.save()
    return jsonify(obj_city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def city_put(city_id):
    """Updates an City object using city_id"""
    obj_city = storage.get("City", city_id)
    if obj_city is None:
        abort(404)

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key != "id" and key != "created_at" and key != "updated_at":
            setattr(obj_city, key, value)
    obj_city.save()
    return jsonify(obj_city.to_dict()), 201

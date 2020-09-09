#!/usr/bin/python3
""" New view for State objects that handles all default RestFul API actions:"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def all_states():
    """Retrieves the list of all State objects"""
    dict_states = []
    for state_obj in storage.all("State").values():
        dict_states.append(state_obj.to_dict())
    return jsonify(dict_states)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def state_id(state_id):
    """ Retrieves a State object based on the state_id """
    dict_state = storage.get("State", state_id)
    if dict_state is None:
        abort(404)
    return jsonify(dict_state.to_dict())


@app_views.route('states/<state_id>', strict_slashes=False, methods=['DELETE'])
def state_deletes(state_id):
    """Deletes an object States"""
    obj_state = storage.get("State", state_id)
    if obj_state is None:
        abort(404)
    storage.delete(obj_state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def states_post():
    """ transform the HTTP body request to a dictionary"""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        abort(400, description="Not a JSON")
    if "name" not in data.keys():
        abort(400, description="Missing name")
    obj_state = State(**data)
    storage.new(obj_state)
    storage.save()
    return jsonify(obj_state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def states_put(state_id):
    """Updates an State object using state_id"""
    obj_state = storage.get("State", state_id)
    if obj_state is None:
        abort(404)

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key != "id" and key != "create_at" and key != "updated_at":
            setattr(obj_state, key, value)
    obj_state.save()
    return jsonify(obj_state.to_dict()), 201

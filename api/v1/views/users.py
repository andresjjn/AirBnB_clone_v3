#!/usr/bin/python3
""" New view for City objects that handles all default RestFul API actions:"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def all_users():
    """Retrieves the list of all User objects"""
    dict_users = []
    for user_obj in storage.all("User").values():
        dict_users.append(user_obj.to_dict())
    return jsonify(dict_users)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def user_id(user_id):
    """ Retrieves a User object based on the user_id """
    dict_user = storage.get("User", user_id)
    if dict_user is None:
        abort(404)
    return jsonify(dict_user.to_dict())


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def user_deletes(user_id):
    """Deletes an object User"""
    obj_user = storage.get("User", user_id)
    if obj_user is None:
        abort(404)
    storage.delete(obj_user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def user_post():
    """ transform the HTTP body request to a dictionary"""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        abort(400, description="Not a JSON")
    if "email" not in data.keys():
        abort(400, description="Missing email")
    if "password" not in data.keys():
        abort(400, description="Missing password")
    obj_user = User(**data)
    storage.new(obj_user)
    storage.save()
    return jsonify(obj_user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def user_put(user_id):
    """Updates an User object using user_id"""
    obj_user = storage.get("User", user_id)
    if obj_user is None:
        abort(404)
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key != "id" and key != "created_at" and key != "updated_at" and\
           key != "email":
            if key == "password":
                obj_user.update_password(value)
            else:
                setattr(obj_user, key, value)
    obj_user.save()
    return jsonify(obj_user.to_dict()), 200

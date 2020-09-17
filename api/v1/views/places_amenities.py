#!/usr/bin/python3
""" Create a new view for the link between Place objects and Amenity objects"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models import *


@app_views.route('/places/<place_id>/amenities',
                 strict_slashes=False, methods=['GET'])
def all_place_amentities(place_id):
    """Retrieves the list of all place objects from a city"""

    dict_amenities = []
    obj_place = storage.get("Place", place_id)

    if obj_place is None:
        abort(404)
    if storage_t == "db":
        for obj_amenity in obj_place.amenities:
            dict_amenities.append(obj_amenity.to_dict())
    else:
        for amenity_id in obj_place.amenity_ids:
            obj_amenity = storage.get("Amenity", amenity_id)
            dict_amenities.append(obj_amenity.to_dict())
    return jsonify(dict_amenities)


@ app_views.route('/places/<place_id>/amenities/<amenity_id>',
                  strict_slashes=False, methods=['POST', 'DELETE'])
def amenity_deletes_and_post(place_id, amenity_id):
    """ Retrieves or deletes an amenity object based on the place_id
        and amenity_id"""

    obj_place = storage.get("Place", place_id)
    obj_amenity = storage.get("Amenity", amenity_id)

    if obj_place is None or obj_amenity is None:
        abort(404)

    if request.method == "DELETE":

        if storage_t == "db":
            if obj_amenity not in obj_place.amenities:
                abort(404)
            obj_place.amenities.remove(obj_amenity)

        else:
            if amenity_id not in obj_place.amenity_ids:
                abort(404)
            obj_place.amenity_ids.remove(amenity_id)
        storage.save()
        return jsonify({}), 200

    if request.method == "POST":

        if storage_t == "db":

            if obj_amenity not in obj_place.amenities:
                obj_place.amenities.append(obj_amenity)
            else:
                storage.save()
                return jsonify(obj_amenity.to_dict()), 200
        else:
            if amenity_id not in obj_place.amenity_ids:
                obj_place.amenity_ids.append(amenity_id)
            else:
                obj_amenity = storage.get("Amenity", amenity_id)
                storage.save()
                return jsonify(obj_amenity.to_dict()), 200

        storage.save()
        return jsonify(obj_amenity.to_dict()), 201

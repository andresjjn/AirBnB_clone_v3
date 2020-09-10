#!/usr/bin/python3
"""New view for Place objects """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def all_reviews(place_id):
    """Retrieves the list of all Review objects from a place"""
    dict_reviews = []
    obj_place = storage.get("Place", place_id)
    if obj_place is None:
        abort(404)
    for obj_review in obj_place.reviews:
        dict_reviews.append(obj_review.to_dict())
    return jsonify(dict_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE'])
def review_id(review_id):
    """ Retrieves or deletes a place object based on the review_id"""

    obj_review = storage.get("Review", review_id)
    if obj_review is None:
        abort(404)
    if request.method == "GET":
        return jsonify(obj_review.to_dict())
    if request.method == "DELETE":
        storage.delete(obj_review)
        storage.save()
        return jsonify({}), 200


@app_views.route('places/<place_id>/reviews', methods=['POST'])
def review_post(place_id):
    """Creates and Add a new review object to a place based on the
    place_id"""

    obj_place = storage.get("Place", place_id)
    if obj_place is None:
        abort(404)
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        abort(400, description="Not a JSON")
    if "user_id" not in data.keys():
        abort(400, description="Missing user_id")
    if "text" not in data.keys():
        abort(400, description="Missing text")

    user_id = data["user_id"]
    obj_user = storage.get("User", user_id)
    if obj_user is None:
        abort(404)

    data["place_id"] = place_id
    obj_review = Review(**data)
    storage.new(obj_review)
    storage.save()
    return jsonify(obj_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def review_delete(review_id):
    """ Retrieves or deletes a review object based on the review_id"""

    obj_review = storage.get("Review", review_id)
    if obj_review is None:
        abort(404)
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        abort(400, description="Not a JSON")

    ignore_keys = ['id', 'created_at', 'updated_at', 'user_id']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(obj_review, key, value)
    obj_review.save()
    return jsonify(obj_review.to_dict()), 200

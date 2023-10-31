#!/usr/bin/python3
"""places review function"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.review import Review
from models.place import Place
from models.user import User
import models


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_all_reviews(place_id):
    """all reviews linked to a place"""
    state = models.storage.get("Place", place_id)
    if state:
        city = models.storage.all("Review")
        all_city = []
        for c in city.values():
            if c.place_id == place_id:
                all_city.append(c.to_dict())
        return jsonify(all_city)
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_a_review_with_id(review_id):
    """retrieve review using id"""
    res = models.storage.get("Review", review_id)
    if res:
        return jsonify(res.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_a_review_with_id(review_id):
    """drop a review using id"""
    res = models.storage.get("Review", review_id)
    if res:
        res.delete()
        models.storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def add_a_review_router(place_id):
    """creates review"""
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in request.json:
        return jsonify({"error": "Missing user_id"}), 400
    if 'text' not in request.json:
        return jsonify({"error": "Missing text"}), 400
    status = models.storage.get("Place", place_id)
    if status is None:
        abort(404)
    userid = request.get_json().get('user_id')
    stat = models.storage.get("User", userid)
    if stat is None:
        abort(404)
    values = request.get_json()
    new_state = Review(**values)
    new_state.place_id = place_id
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_a_review_with_id(review_id):
    """update review using ID"""
    res = models.storage.get("Review", review_id)
    if res:
        if not request.json:
            return jsonify({"error": "Not a JSON"}), 400
        for i, j in request.get_json().items():
            if i not in ['id', 'user_id',
                         'created_at', 'updated_at', 'state_id']:
                setattr(res, i, j)
        res.save()
        return jsonify(res.to_dict()), 200
    abort(404)

#!/usr/bin/python3
"""amenities function"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
import models

@app_views.route('/amenities', methods=['GET'])
def get_all_amenities():
    """get all amenities"""
    all_state = []
    for e in models.storage.all("Amenity").values():
        all_state.append(e.to_dict())
    return jsonify(all_state)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_a_amenity_with_id(amenity_id):
    """get amenity using id"""
    answer = models.storage.get("Amenity", amenity_id)
    if answer:
        return jsonify(answer.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_a_ameniity_with_id(amenity_id):
    """delete amenity using id"""
    answer = models.storage.get("Amenity", amenity_id)
    if answer:
        answer.delete()
        models.storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/amenities', methods=['POST'])
def add_a_amenity():
    """create amenity"""
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    values = request.get_json()
    newState = Amenity(**values)
    newState.save()
    return jsonify(newState.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_a_amenity_with_id(amenity_id):
    """get amenity using id"""
    answer = models.storage.get("Amenity", amenity_id)
    if answer:
        if not request.json:
            return jsonify({"error": "Not a JSON"}), 400
        for i, j in request.get_json().items():
            if i not in ['id', 'created_at', 'updated_at']:
                setattr(answer, i, j)
        answer.save()
        return jsonify(answer.to_dict()), 200
    abort(404)

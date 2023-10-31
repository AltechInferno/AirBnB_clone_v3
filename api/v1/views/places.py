#!/usr/bin/python3
"""Create places function"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.city import City
from models.place import Place
from models.user import User
import models


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_all_places(city_id):
    """get all places linked to a city"""
    state = models.storage.get("City", city_id)
    if state:
        city = models.storage.all("Place")
        all_city = []
        for ct in city.values():
            if ct.city_id == city_id:
                all_city.append(ct.to_dict())
        return jsonify(all_city)
    abort(404)


@app_views.route('places/<place_id>', methods=['GET'])
def get_a_place_with_id(place_id):
    """get place using id"""
    res = models.storage.get("Place", place_id)
    if res:
        return jsonify(res.to_dict())
    abort(404)


@app_views.route('places/<place_id>', methods=['DELETE'])
def delete_a_place_with_id(place_id):
    """delete place using id"""
    res = models.storage.get("Place", place_id)
    if res:
        res.delete()
        models.storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def add_a_place_router(city_id):
    """create place"""
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in request.json:
        return jsonify({"error": "Missing user_id"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    status = models.storage.get("City", city_id)
    if status is None:
        abort(404)
    userid = request.get_json().get('user_id')
    stat = models.storage.get("User", userid)
    if stat is None:
        abort(404)
    values = request.get_json()
    newState = Place(**values)
    newState.city_id = city_id
    newState.save()
    return jsonify(newState.to_dict()), 201


@app_views.route('places/<place_id>', methods=['PUT'])
def update_a_place_with_id(place_id):
    """get city using id"""
    res = models.storage.get("Place", place_id)
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

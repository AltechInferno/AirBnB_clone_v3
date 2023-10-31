#!/usr/bin/python3
"""users function"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
import models


@app_views.route('/users', methods=['GET'])
def get_all_users():
    """get all users"""
    all_state = []
    for enu in models.storage.all("User").values():
        all_state.append(enu.to_dict())
    return jsonify(all_state)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_a_user_with_id(user_id):
    """get user using id"""
    res = models.storage.get("User", user_id)
    if res:
        return jsonify(res.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_a_user_with_id(user_id):
    """delete state using id"""
    res = models.storage.get("User", user_id)
    if res:
        res.delete()
        models.storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/users', methods=['POST'])
def add_a_user():
    """create user"""
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in request.json:
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in request.json:
        return jsonify({"error": "Missing password"}), 400
    values = request.get_json()
    newState = User(**values)
    newState.save()
    return jsonify(newState.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_a_user_with_id(user_id):
    """update user using id"""
    res = models.storage.get("User", user_id)
    if res:
        if not request.json:
            return jsonify({"error": "Not a JSON"}), 400
        for i, j in request.get_json().items():
            if i not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(res, i, j)
        res.save()
        return jsonify(res.to_dict()), 200
    abort(404)

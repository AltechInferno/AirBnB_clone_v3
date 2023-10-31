#!/usr/bin/python3
"""states function"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
import models


@app_views.route('/states', methods=['GET'])
def get_all_states():
    """get all state"""
    all_state = []
    for enu in models.storage.all("State").values():
        all_state.append(enu.to_dict())
    return jsonify(all_state)


@app_views.route('states/<state_id>', methods=['GET'])
def get_a_state_with_id(state_id):
    """get state using id"""
    res = models.storage.get("State", state_id)
    if res:
        return jsonify(res.to_dict())
    abort(404)


@app_views.route('states/<state_id>', methods=['DELETE'])
def delete_a_state_with_id(state_id):
    """delete state using id"""
    res = models.storage.get("State", state_id)
    if res:
        res.delete()
        models.storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states', methods=['POST'])
def add_a_statesi():
    """create state"""
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    values = request.get_json()
    newState = State(**values)
    newState.save()
    return jsonify(newState.to_dict()), 201


@app_views.route('states/<state_id>', methods=['PUT'])
def update_a_state_with_id(state_id):
    """get state using id"""
    res = models.storage.get("State", state_id)
    if res:
        if not request.json:
            return jsonify({"error": "Not a JSON"}), 400
        for i, j in request.get_json().items():
            if i not in ['id', 'created_at', 'updated_at']:
                setattr(res, i, j)
        res.save()
        return jsonify(res.to_dict()), 200
    abort(404)

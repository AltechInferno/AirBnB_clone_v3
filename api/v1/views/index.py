#!/usr/bin/python3
"""router of the app_views"""

from api.v1.views import app_views
from flask import jsonify
import models


@app_views.route('/status', strict_slashes=False)
def get_status():
    """status of the app"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def status_page():
    """status of each model"""
    model = models.storage
    res = {'cities': model.count("City"),
           'places': model.count("Place"),
           'reviews': model.count("Review"),
           'states': model.count("State"),
           'users': model.count("User"),
	  'amenities': model.count("Amenity")}
    return jsonify(res)

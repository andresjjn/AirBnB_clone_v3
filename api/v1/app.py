#!/usr/bin/python3
""" This file contain code that allow check the status of the AirBnB_clone API
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={
    r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)

h = getenv('HBNB_API_HOST', '0.0.0.0')
p = getenv('HBNB_API_PORT', '5000')


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """Handler for 404 errors that returns a JSON-formatted
       404 status code response"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=h, port=p, threaded=True)

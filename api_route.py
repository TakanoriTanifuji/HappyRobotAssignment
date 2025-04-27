from flask import Flask, jsonify, request
import csv
import json
import os
from functools import wraps

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")

def require_api_key(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        provided_key = request.headers.get('X-API-Key')
        print(API_KEY)
        if provided_key == API_KEY:
            return function(*args, **kwargs)
        return jsonify({"error": "Invalid API key"}), 401
    return decorated

@app.route("/loads/<string:referece_number>")
@require_api_key
def get_loads(referece_number):
    with open("loads.csv", "r") as file:
      data = csv.DictReader(file)
      for row in data:
        if row["reference_number"] == str(referece_number):
          return jsonify(row)
    return jsonify({"error": "Load not found"}), 404
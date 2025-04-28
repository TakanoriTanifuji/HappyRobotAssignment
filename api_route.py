from flask import Flask, jsonify, request
import csv
import json
import os
import requests
from functools import wraps

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")
FMCSA_API_KEY = os.environ.get("FMCSA_API_KEY")

def require_api_key(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        provided_key = request.headers.get('X-API-Key')
        print(API_KEY)
        if provided_key == API_KEY:
            return function(*args, **kwargs)
        return jsonify({"error": "Invalid API key"}), 401
    return decorated

@app.route("/carrier/<string:mc_number>")
@require_api_key
def get_carrier(mc_number):
    try:
        url = f"https://mobile.fmcsa.dot.gov/qc/services/carriers/docket-number/{mc_number}"
        response = requests.get(url, params={"webKey":FMCSA_API_KEY})
        if response.status_code == 200:
          response = response.json()

          if response["content"] == []:
            return jsonify({"error": "Carrier not found"}), 404
          
          carrier_data = response["content"][0]["carrier"]
          data = {
            "legal_name": carrier_data["legalName"],
            "phy_city": carrier_data["phyCity"],
            "phy_state": carrier_data["phyState"],
            "phy_street": carrier_data["phyStreet"],
            "phy_zip": carrier_data["phyZipcode"],
          }
          return jsonify(data)
        else:
          return jsonify({"FMCSA API error": response.text}), response.status_code
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500  
   
@app.route("/loads/<string:referece_number>")
@require_api_key
def get_loads(referece_number):
    try:
      with open("loads.csv", "r") as file:
        data = csv.DictReader(file)
        for row in data:
          if row["reference_number"] == str(referece_number):
            return jsonify(row)
        return jsonify({"error": "Load not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

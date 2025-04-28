from flask import Flask, jsonify, request
import os
import requests
import pandas as pd
from functools import wraps

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")
FMCSA_API_KEY = os.environ.get("FMCSA_API_KEY")

def require_api_key(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        provided_key = request.headers.get('X-API-Key')
        if provided_key == API_KEY:
            return function(*args, **kwargs)
        return jsonify({"error": "Invalid API key"}), 401
    return decorated

@app.route("/carrier/<string:mc_number>")
@require_api_key
def get_carrier(mc_number):
    try:
        # Retrieve carrier information from FMCSA REST API
        url = f"https://mobile.fmcsa.dot.gov/qc/services/carriers/docket-number/{mc_number}"
        response = requests.get(url, params={"webKey":FMCSA_API_KEY})
        if response.status_code == 200:
          response = response.json()

          # if the mc number does not exist, the response will be an empty array
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

@app.route("/loads/<string:reference_number>")
@require_api_key
def get_loads(reference_number):
    chunksize = 5000
    csv_file = 'loads.csv'
    # Retrieve load by reference number using chunked CSV processing
    try:
      for chunk in pd.read_csv(csv_file, chunksize=chunksize):
        matching_rows = chunk[chunk['reference_number'] == reference_number]
        if not matching_rows.empty:
          row = matching_rows.iloc[0].to_dict()
          return jsonify(row)
      return jsonify({"error": "Load not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
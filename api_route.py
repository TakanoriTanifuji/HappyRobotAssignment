from flask import Flask, jsonify
import csv
import json
app = Flask(__name__)

@app.route("/loads/<string:referece_number>")
def get_loads(referece_number):
    with open("loads.csv", "r") as file:
      data = csv.DictReader(file)
      for row in data:
        if row["reference_number"] == str(referece_number):
          return jsonify(row)
    return jsonify({"error": "Load not found"}), 404

if __name__ == '__main__':
   app.run(debug = True)
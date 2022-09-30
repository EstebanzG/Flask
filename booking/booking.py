from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
   bookings = json.load(jsf)["bookings"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"

@app.route("/bookings", methods=['GET'])
def get_json():
   res = make_response(jsonify(bookings), 200)
   return res

@app.route("/bookings/<userid>", methods=['GET'])
def get_booking_for_user(userid):
    for b in bookings:
        if str(b["userid"]) == str(userid):
            res = make_response(jsonify(b),200)
            return res
    return make_response(jsonify({"error":"bad input parameter"}),400)

@app.route("/bookings/<userid>", methods=['POST'])
def add_booking_byuser(userid):
    req = request.get_json()
    for userDates in bookings:
        if str(userDates["userid"]) == str(userid):
            for dateMovies in userDates["dates"]:
                if str(req["date"]) == dateMovies["date"]:
                    if str(req["movie"]) not in dateMovies["movies"]:
                        dateMovies["movies"].append(str(req["movie"]))
                        res = make_response(jsonify({"message": "Booking created"}), 200)
                        return res
                    else:
                        res = make_response(jsonify({"message": "an existing item already exists"}), 409)
                        return res
            userDates["dates"].append({"date": req["date"], "movies": [req["movie"]]})
            res = make_response(jsonify({"message": "Booking created"}), 200)
            return res

    res = make_response(jsonify({"message": "User not exists"}), 404)
    return res

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)

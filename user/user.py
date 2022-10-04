from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

with open('{}/databases/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]
@app.route("/documentation", methods=['GET'])
def user_documentation(userid):
    return make_response(jsonify({"Error": "user not exist"}), 400)
@app.route("/bookingsbyuserid/<userid>", methods=['GET'])
def bookingsbyuserid(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            bookings = requests.get('http://localhost:3201/bookings/' + userid)
            if bookings.status_code == 200:
                bookings = bookings.json()
                return make_response(bookings, 200)
            return make_response(jsonify({"Error": "User don't have booking"}), 400)
    return make_response(jsonify({"Error": "user not exist"}), 400)
@app.route("/bookingsdetailbyuserid/<userid>", methods=['GET'])
def bookingsdetailbyuserid(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            bookings = requests.get('http://localhost:3201/bookings/' + userid)
            if bookings.status_code == 200:
                bookings = bookings.json()
                for date in bookings["dates"]:
                    movieDetail = []
                    for movie in date["movies"]:
                        movieDetail.append(requests.get('http://localhost:3230/movies/' + movie).json())
                    date["movies"] = movieDetail
                return make_response(bookings, 200)
            return make_response(jsonify({"Error": "User don't have booking"}), 400)
    return make_response(jsonify({"Error": "User not exist"}), 400)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)

from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

with open('{}/databases/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]


# Help route : GET : http://localhost:3203/help
@app.route("/help", methods=['GET'])
def help():
    return make_response(render_template('help.html', body_text='This is my HTML help documentation for User service'), 200)


# Get bookings by user id : GET : http://localhost:3203/bookings_by_user_id/garret_heaton
@app.route("/bookings_by_user_id/<userid>", methods=['GET'])
def bookings_by_user_id(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            bookings = requests.get('http://localhost:3201/bookings/' + userid)
            if bookings.status_code == 200:
                bookings = bookings.json()
                return make_response(bookings, 200)
            return make_response(jsonify({"Error": "User don't have booking"}), 401)
    return make_response(jsonify({"Error": "User not exist"}), 402)


# Get bookings withs details by user id : GET : http://localhost:3203/bookings_details_by_user_id/garret_heaton
@app.route("/bookings_details_by_user_id/<userid>", methods=['GET'])
def bookings_details_by_user_id(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            bookings = requests.get('http://localhost:3201/bookings/' + userid)
            if bookings.status_code == 200:
                bookings = bookings.json()
                for date in bookings["dates"]:
                    movieDetail = []
                    for movie in date["movies"]:
                        movieDetail.append(requests.get('http://localhost:3200/movies/' + movie).json())
                    date["movies"] = movieDetail
                return make_response(bookings, 200)
            return make_response(jsonify({"Error": "User don't have booking"}), 401)
    return make_response(jsonify({"Error": "User not exist"}), 402)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)

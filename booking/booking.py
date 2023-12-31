from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
    bookings = json.load(jsf)["bookings"]


# Welcome route : GET : http://localhost:3201/
@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"


# Help route : GET : http://localhost:3200/help
@app.route("/help", methods=['GET'])
def help():
    return make_response(
        render_template('help.html', body_text='This is my HTML help documentation for Booking service'),
        200)


# Get all json database route : GET : http://localhost:3200/bookings
@app.route("/bookings", methods=['GET'])
def get_json():
    res = make_response(jsonify(bookings), 200)
    return res


# Get booking by id route : GET : http://localhost:3200/bookings/garret_heaton
@app.route("/bookings/<user_id>", methods=['GET'])
def get_booking_for_user(user_id):
    for b in bookings:
        if str(b["userid"]) == str(user_id):
            res = make_response(jsonify(b), 200)
            return res
    return make_response(jsonify({"error": "User id not found, you should check /bookings"}), 400)


# Nous n'avons pas eu le temps de revoir le code de cette fonction
# Nous sommes conscient qu'elle ne peut qu'être optimisée
# Add booking to user by his id route
# ↓ Postman
# POST : http://localhost:3200/bookings/garret_heaton
# Body Raw Json :
"""
{
  "date": "20151201",
  "movieid": "276c79ec-a26a-40a6-b3d3-fb242a5947b6"
}
"""


@app.route("/bookings/<userid>", methods=['POST'])
def add_booking_by_user(userid):
    req = request.get_json()
    for userDates in bookings:
        # si l'utilisateur a déjà des réservations
        if str(userDates["userid"]) == str(userid):

            # pour tous les couples date movie[]
            for dateMovies in userDates["dates"]:

                # si l'utilisateur à deja des resa à cette date
                if str(req["date"]) == dateMovies["date"]:

                    # si le movie n'est pas deja reservé à cette date
                    if str(req["movieid"]) not in dateMovies["movies"]:

                        # vérifie s'il est programmé à cette date
                        moviesShowDate = requests.get('http://localhost:3202/showtimes/' + dateMovies["date"])
                        if moviesShowDate.status_code == 200:
                            if str(req["movieid"]) in (moviesShowDate.json())["movies"]:
                                dateMovies["movies"].append(str(req["movie"]))
                                res = make_response(jsonify({"message": "Booking created"}), 200)
                                return res
                            else:
                                res = make_response(jsonify({"error": "This movie is not at this showtime"}), 401)
                                return res
                        else:
                            res = make_response(jsonify({"error": "No movie at this showtime"}), 402)
                            return res
                    else:
                        res = make_response(jsonify({"error": "You already booked this movie"}), 403)
                        return res

            moviesShow = requests.get('http://localhost:3202/showtimes')
            for mv in moviesShow.json():
                if str(req["date"]) == mv["date"]:
                    if str(req["movieid"]) in mv["movies"]:
                        userDates["dates"].append({"date": req["date"], "movies": [req["movieid"]]})
                        res = make_response(jsonify({"message": "Booking created"}), 200)
                        return res
            res = make_response(jsonify({"error": "Showtime or movie at this showtime not exists"}), 404)
            return res

    # sinon on dit que l'utilisateur n'existe pas
    res = make_response(jsonify({"message": "User id not found, you should check /bookings"}), 405)
    return res


if __name__ == "__main__":
    print("Server running in port %s" % PORT)
    app.run(host=HOST, port=PORT)

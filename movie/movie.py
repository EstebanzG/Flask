from flask import Flask, render_template, request, jsonify, make_response
import json
import sys
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3200
HOST = '0.0.0.0'

with open('{}/databases/movies.json'.format("."), "r") as jsf:
    movies = json.load(jsf)["movies"]


# Welcome route : GET : http://localhost:3200/
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>", 200)


# Help route : GET : http://localhost:3200/help
@app.route("/help", methods=['GET'])
def help():
    return make_response(render_template('help.html', body_text='This is my HTML help documentation for Movie service'),
                         200)


# Template route : GET : http://localhost:3200/template
@app.route("/template", methods=['GET'])
def template():
    return make_response(render_template('index.html', body_text='This is my HTML template for Movie service'), 200)


# Get all json database route : GET : http://localhost:3200/json
@app.route("/json", methods=['GET'])
def get_json():
    res = make_response(jsonify(movies), 200)
    return res


# Get movie by id route : GET : http://localhost:3200/movies/720d006c-3a57-4b6a-b18f-9b713b073f3c
@app.route("/movies/<movie_id>", methods=['GET'])
def get_movie_byid(movie_id):
    for movie in movies:
        if str(movie["id"]) == str(movie_id):
            res = make_response(jsonify(movie), 200)
            return res
    return make_response(
        jsonify({"error": "Movie ID not found, you should create a movie by '/movies/<movie_id>' post route."}), 400)


# Get movie by id route
# ↓ Postman
# GET : http://localhost:3200/movies_by_title
# Key : title
# Value : The Good Dinosaur
@app.route("/movies_by_title", methods=['GET'])
def get_movie_by_title():
    jsonRes = ""
    if request.args:
        req = request.args
        for movie in movies:
            if str(movie["title"]) == str(req["title"]):
                jsonRes = movie
    if not jsonRes:
        res = make_response(jsonify({"error": "movie title not found, you should create a movie by "
                                              "'/movies/<movie_id>' post route"}), 400)
    else:
        res = make_response(jsonify(jsonRes), 200)
    return res


# Get movie by rate route
# ↓ Postman
# GET : http://localhost:3200/movies_by_rate
# Key : rating
# Value : 7.4
@app.route("/movies_by_rate", methods=['GET'])
def get_movie_by_rate():
    jsonRes = []
    if request.args:
        req = request.args
        for movie in movies:
            if float(movie["rating"]) == float(req["rating"]):
                jsonRes.append(movie)
    if not jsonRes:
        res = make_response(
            jsonify({"error": "movie with this rate not found, you should check movies by '/json' get route"}), 400)
    else:
        res = make_response(jsonify(jsonRes), 200)
    return res


# Create movie by id route
# ↓ Postman
# POST : http://localhost:3200/movies/1
# Body Raw Json :
"""
    {
        "director": "Antoine",
        "id": "1",
        "rating": 7.4,
        "title": "ArchiDistribute"
    }
"""


@app.route("/movies/<movie_id>", methods=['POST'])
def create_movie(movie_id):
    req = request.get_json()
    for movie in movies:
        if str(movie["id"]) == str(movie_id):
            return make_response(jsonify({"error": "an existing item already exists"}), 409)
    movies.append(req)
    res = make_response(jsonify(req), 200)
    return res


# Change movie rate by id route
# ↓ Postman
# PUT : http://localhost:3200/movies/1/5.2
# Body Raw Json :
"""
    {
        "director": "Antoine",
        "id": "1",
        "rating": 5.2,
        "title": "ArchiDistribute"
    }
"""


@app.route("/movies/<movie_id>/<rate>", methods=['PUT'])
def update_movie_rating(movie_id, rate):
    for movie in movies:
        if str(movie["id"]) == str(movie_id):
            movie["rating"] = float(rate)
            res = make_response(jsonify(movie), 200)
            return res
    res = make_response(jsonify({"error": "movie ID not found, you should check movies by '/json' get route"}), 400)
    return res


# Delete movie by id route
# ↓ Postman
# DELETE : http://localhost:3200/movies/1
@app.route("/movies/<movie_id>", methods=['DELETE'])
def delete_movie(movie_id):
    for movie in movies:
        if str(movie["id"]) == str(movie_id):
            movies.remove(movie)
            return make_response(jsonify(movie), 200)
    res = make_response(jsonify({"error": "movie ID not found, you should check movies by '/json' get route"}), 400)
    return res


if __name__ == "__main__":
    print("Server running in port %s" % PORT)
    app.run(host=HOST, port=PORT)

from flask import Flask, render_template, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3202
HOST = '0.0.0.0'

with open('{}/databases/times.json'.format("."), "r") as jsf:
    schedule = json.load(jsf)["schedule"]


# Welcome route : GET : http://localhost:3202/
@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the Showtime service!</h1>"


# Help route : GET : http://localhost:3202/help
@app.route("/help", methods=['GET'])
def help():
    return make_response(render_template('help.html', body_text='This is my HTML help documentation for Showtimes service'), 200)


# Get all showtimes json database route : GET : http://localhost:3202/showtimes
@app.route("/showtimes", methods=['GET'])
def get_schedule():
    res = make_response(jsonify(schedule), 200)
    return res


# Get showtimes by date route : GET : http://localhost:3202/showtimes/20151130
@app.route("/showtimes/<date>", methods=['GET'])
def get_movies_by_date(date):
    for s in schedule:
        if str(s["date"]) == str(date):
            res = make_response(jsonify(s), 200)
            return res
    return make_response(jsonify({"error": "No showtime for this date, check /showtimes route"}), 400)


if __name__ == "__main__":
    print("Server running in port %s" % PORT)
    app.run(host=HOST, port=PORT)

from flask import Flask, jsonify, request
from time import sleep
from ORM import Operations
app = Flask(__name__)


@app.route('/cities')
def cities():
  return jsonify({ 'cities': Operations.GetCities() })

@app.route('/tours')
def tours():
  city = request.args.get('city', default = 0, type = int)
  return jsonify({ 'tours':  Operations.GetTourByCity(city)})

@app.route('/tours/tour')
def tour():
  tour = request.args.get('tour', default = 0, type = int)
  return jsonify({ 'tours':  Operations.GetTour(tour)})

if __name__ == "__main__":
  tour()
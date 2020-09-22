from flask import Flask, jsonify, request
from time import sleep
from ORM import Operations
from flask_cors import CORS, cross_origin
import os
from json import loads
from pprint import pprint


app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"*": {"origins": os.environ.get('WEB')}})

@app.route('/cities')
def cities():
  return jsonify(Operations.GetCities())

@app.route('/cities/add')
def add_city():
  city = request.args.get('city', default = 0, type = str)
  Operations.SaveCity(city)
  return jsonify(Operations.GetCities())

@app.route('/tours')
def tours():
  city = request.args.get('city', default = 0, type = int)
  return jsonify({ 'tours':  Operations.GetTourByCity(city)})

@app.route('/tours/tour')
def tour():
  tour = request.args.get('tour', default = 0, type = int)
  return jsonify({ 'tours':  Operations.GetTour(tour)})

@app.route('/tours/tour/save')
def add_tour():
  tour = loads(request.args.get('tour', default = None, type = str))
  Operations.SaveTour(tour)
  return jsonify({ 'heh': 1 })

if __name__ == "__main__":
  tour()
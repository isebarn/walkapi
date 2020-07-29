from flask import Flask, jsonify
from time import sleep
from ORM import Operations
app = Flask(__name__)


@app.route('/')
def cities():
  return 'Hello'

if __name__ == "__main__":
  print(a)
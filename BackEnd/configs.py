from flask import Flask
from flask_pymongo import PyMongo

application = Flask( __name__)
client = PyMongo(application, uri="mongodb://localhost:27017/CleanAirZone")
db = client.db
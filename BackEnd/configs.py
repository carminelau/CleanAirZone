from flask import Flask
from flask_pymongo import PyMongo
from pymongo import MongoClient

application = Flask( __name__)

client = MongoClient('localhost', 27017)

db = client.CleanAirZone
from flask import Flask
from flask_pymongo import PyMongo

application = Flask( __name__)
application.config["MONGO_URI"] = "mongodb+srv://root:root@cluster0.litxc.mongodb.net/test"

mongo = PyMongo(application)

db=mongo.db
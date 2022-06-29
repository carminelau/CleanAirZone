from flask import Flask
from flask_pymongo import PyMongo
from flask_compress import Compress

application = Flask( __name__)
application.config["MONGO_URI"] = "mongodb+srv://root:root@cluster0.litxc.mongodb.net/CleanAirZone"
application.config["COMPRESS_ALGORITHM"] = 'gzip'  # disable default compression of all eligible requests



mongo = PyMongo(application)


db=mongo.db
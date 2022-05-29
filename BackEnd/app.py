from flask import Flask, request
import pandas as pd
from databases import particulateData,stations,weatherData
from tools import findCountry
import json

app = Flask(__name__)

@app.route('/')
def home():
    return "home"

@app.route("/getCountry")
def getCountry():
    df = pd.DataFrame(list(findCountry()))

    return df.to_json();

@app.route("/getStationsByCountry")
def getStationByCountry():
    country = request.args.get('country')
    if(country==""):
        return {"error" : "Country non inserto"}
    
    dati=stations.find({"country" : country})
    df = pd.DataFrame(dati)
    return str(df.to_string())

if __name__ == '__main__':
    app.run(debug = True, port= 5600)
    
from flask import Flask,jsonify,request
import pandas as pd
from databases import particulateData,stations,weatherData,country
from tools import findCountry
import json
import pycountry
import datetime
from flask_cors import CORS
import requests


app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "home"

@app.route("/getCountry")
def getCountry():
    nazioni=country.find()
    array=[]
    for item in nazioni:
        del item['_id']
        array.append(item)

    return jsonify(array)

@app.route("/getStationsByCountry")
def getStationByCountry():
    count = request.args.get('country')
    if(count==""):
        return jsonify({"error" : "Country non inserto"})
    
    dati=stations.find({"country" : count})
    c = country.find_one({"alpha_2" : count})
    diz={}
    array=[]
    for item in dati:
        del item['_id']
        array.append(item)
    del c['_id']
    diz['country'] = c
    diz['stazioni'] = array
    return jsonify(diz)

@app.route("/getAllStations")
def getAllStations():
    
    dati=stations.find() 
    array=[]
    for item in dati:
        del item['_id']
        array.append(item)
    return jsonify(array)

@app.route("/getDataDayfromId")
def getDataDayfromId():
    id = request.args.get('id')
    if(id==""):
        return jsonify({"error" : "Id non inserto"})
    
    array=[]
    stazione=stations.find_one({"ID" : id}) 
    if stazione['particulate'] == True:
        dati=particulateData.find({'latitude': stazione['latitude'], 'longitude': stazione['longitude']})
        for item in dati:
            del item['_id']
            data= datetime.datetime.strptime(item['timestamp'],"%Y-%m-%d %H:%M:%S")
            now= datetime.datetime.now()
            if (data.date() == now.date()):
                array.append(item)
            else:
                return jsonify({"error" : "Dati non trovati"})
    if stazione['weather'] == True:
        dati=weatherData.find({'latitude': stazione['latitude'], 'longitude': stazione['longitude']})
        for item in dati:
            del item['_id']
            data= datetime.datetime.strptime(item['timestamp'],"%Y-%m-%d %H:%M:%S")
            now= datetime.datetime.now()
            if (data.date() == now.date()):
                array.append(item)
            else:
                return jsonify({"error" : "Dati non trovati"})

    return jsonify(array)

@app.route("/getDataWeekfromId")
def getDataWeekfromId():
    id = request.args.get('id')
    if(id==""):
        return jsonify({"error" : "Id non inserto"})
    
    array=[]
    stazione=stations.find_one({"ID" : id}) 
    if stazione['particulate'] == True:
        dati=particulateData.find({'ID': id})
        for item in dati:
            del item['_id']
            data= datetime.datetime.strptime(item['timestamp'],"%Y-%m-%d %H:%M:%S")
            sevenago= datetime.datetime.now() - datetime.timedelta(days = 7)
            if (data.date() >= sevenago.date()):
                array.append(item)
            else:
                return jsonify({"error" : "Dati non trovati"})
    if stazione['weather'] == True:
        dati=weatherData.find({'ID': id})
        for item in dati:
            del item['_id']
            data= datetime.datetime.strptime(item['timestamp'],"%Y-%m-%d %H:%M:%S")
            sevenago= datetime.datetime.now() - datetime.timedelta(days = 7)
            if (data.date() >= sevenago.date()):
                array.append(item)
            else:
                return jsonify({"error" : "Dati non trovati"})

    return jsonify(array)

@app.route("/getParticulateDataDayfromCountry")
def getParticulateDataDayfromCountry():
    country = request.args.get('country')
    if(country==""):
        return jsonify({"error" : "country non inserto"})
    
    array=[]
    stazioni=stations.find({"country" : country})
    
    for stazione in stazioni:
        if stazione['particulate'] == True:
            dati=particulateData.find({'latitude': stazione['latitude'], 'longitude': stazione['longitude']})
            for item in dati:
                del item['_id']
                data= datetime.datetime.strptime(item['timestamp'],"%Y-%m-%d %H:%M:%S")
                now= datetime.datetime.now()
                if (data.date() == now.date()):
                    array.append(item)
    if (len(array)>0):
        return jsonify(array)
    else:
        return jsonify({"error" : "Dati non trovati"})

@app.route("/getWeatherDataDayfromCountry")
def getWeatherDataDayfromCountry():
    country = request.args.get('country')
    if(country==""):
        return jsonify({"error" : "country non inserto"})
    
    array=[]
    stazioni=stations.find({"country" : country})
    for stazione in stazioni:
        if stazione['weather'] == True:
            dati=weatherData.find({'latitude': stazione['latitude'], 'longitude': stazione['longitude']})
            for item in dati:
                del item['_id']
                data= datetime.datetime.strptime(item['timestamp'],"%Y-%m-%d %H:%M:%S")
                now= datetime.datetime.now()
                if (data.date() == now.date()):
                    array.append(item)
    if (len(array)>0):
        return jsonify(array)
    else:
        return jsonify({"error" : "Dati non trovati"})

@app.route("/getWeatherDataDayfromCity")
def getWeatherDataDayfromCity():
    city = request.args.get('city')
    if(city==""):
        return jsonify({"error" : "city non inserto"})
    
    array=[]
    stazioni=stations.find({"city" : city})
    for stazione in stazioni:
        if stazione['weather'] == True:
            dati=weatherData.find({'latitude': stazione['latitude'], 'longitude': stazione['longitude']})
            for item in dati:
                del item['_id']
                data= datetime.datetime.strptime(item['timestamp'],"%Y-%m-%d %H:%M:%S")
                now= datetime.datetime.now()
                if (data.date() == now.date()):
                    array.append(item)
    if (len(array)>0):
        return jsonify(array)
    else:
        return jsonify({"error" : "Dati non trovati"})

@app.route("/getParticulateDataDayfromCity")
def getParticulateDataDayfromCity():
    city = request.args.get('city')
    if(city==""):
        return jsonify({"error" : "city non inserto"})
    
    array=[]
    stazioni=stations.find({"city" : city})
    for stazione in stazioni:
        if stazione['weather'] == True:
            dati=particulateData.find({'latitude': stazione['latitude'], 'longitude': stazione['longitude']})
            for item in dati:
                del item['_id']
                data= datetime.datetime.strptime(item['timestamp'],"%Y-%m-%d %H:%M:%S")
                now= datetime.datetime.now()
                if (data.date() == now.date()):
                    array.append(item)
    if (len(array)>0):
        return jsonify(array)
    else:
        return jsonify({"error" : "Dati non trovati"})

@app.route("/getWeatherDataWeekfromCity")
def getWeatherDataWeekfromCity():
    city = request.args.get('city')
    if(city==""):
        return jsonify({"error" : "city non inserto"})
    
    array=[]
    stazioni=stations.find({"citta" : city})
    for stazione in stazioni:
        if stazione['weather'] == True:
            dati=weatherData.find({'latitude': stazione['latitude'], 'longitude': stazione['longitude']})
            for item in dati:
                del item['_id']
                data= datetime.datetime.strptime(item['timestamp'],"%Y-%m-%d %H:%M:%S")
                sevenago= datetime.datetime.now() - datetime.timedelta(days=7)
                if (data.date() >= sevenago.date()):
                    array.append(item)
    if (len(array)>0):
        return jsonify(array)
    else:
        return jsonify({"error" : "Dati non trovati"})

@app.route("/getParticulateDataWeekfromCity")
def getParticulateDataWeekfromCity():
    city = request.args.get('city')
    if(city==""):
        return jsonify({"error" : "city non inserto"})
    
    array=[]
    stazioni=stations.find({"citta" : city})
    for stazione in stazioni:
        if stazione['particulate'] == True:
            dati=particulateData.find({'latitude': stazione['latitude'], 'longitude': stazione['longitude']})
            for item in dati:
                del item['_id']
                data= datetime.datetime.strptime(item['timestamp'],"%Y-%m-%d %H:%M:%S")
                sevenago= datetime.datetime.now() - datetime.timedelta(days=7)
                if (data.date() >= sevenago.date()):
                    array.append(item)
    if (len(array)>0):
        return jsonify(array)
    else:
        return jsonify({"error" : "Dati non trovati"})

@app.route("/getRegionbyCountry")
def getRegionbyCountry():
    country = request.args.get('country')
    if(country==""):
        return jsonify({"error" : "country non inserto"})
    array=[]
    stazioni=stations.find({"country" : country})
    for stazione in stazioni:
        array.append(stazione['regione'])

    final_array = list(dict.fromkeys(array))
    if (len(final_array)>0):
        return jsonify(final_array)
    else:
        return jsonify({"error" : "Regioni non trovate per" + str(country)})

@app.route("/getProvincebyCountryandRegion")
def getProvincebyCountryandRegion():
    country = request.args.get('country')
    regione = request.args.get('regione')
    if(country==""):
        return jsonify({"error" : "country non inserto"})
    if(regione==""):
        return jsonify({"error" : "regione non inserto"})
    array=[]
    stazioni=stations.find({"country" : country, "regione": regione})
    for stazione in stazioni:
        array.append(stazione['provincia'])

    final_array = list(dict.fromkeys(array))
    if (len(final_array)>0):
        return jsonify(final_array)
    else:
        return jsonify({"error" : "Province non trovate per" + str(regione)})

@app.route("/getCitybyCountryandRegionandProvince")
def getCitybyCountryandRegionandProvince():
    country = request.args.get('country')
    regione = request.args.get('regione')
    provincia = request.args.get('provincia')

    if(country==""):
        return jsonify({"error" : "country non inserto"})
    if(regione==""):
        return jsonify({"error" : "regione non inserto"})
    if(provincia==""):
        return jsonify({"error" : "provincia non inserto"})
    array=[]
    stazioni=stations.find({"country" : country, "regione": regione, "provincia":provincia})
    for stazione in stazioni:
        array.append(stazione['citta'])

    final_array = list(dict.fromkeys(array))
    if (len(final_array)>0):
        return jsonify(final_array)
    else:
        return jsonify({"error" : "Province non trovate per" + str(provincia)})

@app.route("/CountSensorItaly")
def CountSensorItaly():    
    dati=stations.count_documents({"country" : 'IT'}) 
    return jsonify({"dati":dati})

@app.route("/CountSensor")
def CountSensor():    
    dati=stations.count_documents({}) 
    return jsonify({"dati":dati})

@app.route("/CountDataWorld")
def CountDataWorld():    
    datipartculate=particulateData.count_documents({})
    datiweather=weatherData.count_documents({}) 
    return jsonify({"dati":datipartculate+datiweather})


if __name__ == '__main__':
    app.run(debug = True, port= 5600)
    
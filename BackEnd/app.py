from flask import Flask, request,jsonify
import pandas as pd
from databases import particulateData,stations,weatherData
from tools import findCountry
import json
import pycountry
import datetime


app = Flask(__name__)

@app.route('/')
def home():
    return "home"

@app.route("/getCountry")
def getCountry():
    array={}
    for item in findCountry():
        array[item]=pycountry.countries.get(alpha_2=item).name

    return jsonify(array)

@app.route("/getStationsByCountry")
def getStationByCountry():
    country = request.args.get('country')
    if(country==""):
        return jsonify({"error" : "Country non inserto"})
    
    dati=stations.find({"country" : country}) 
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
        dati=particulateData.find({'ID': id})
        for item in dati:
            del item['_id']
            data= datetime.datetime.strptime(item['timestamp'],"%Y-%m-%d %H:%M:%S")
            now= datetime.datetime.now()
            if (data.date() == now.date()):
                array.append(item)
            else:
                return jsonify({"error" : "Dati non trovati"})
    if stazione['weather'] == True:
        dati=weatherData.find({'ID': id})
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
            dati=particulateData.find({'ID': stazione['ID']})
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
            dati=weatherData.find({'ID': stazione['ID']})
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
            dati=weatherData.find({'ID': stazione['ID']})
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
            dati=particulateData.find({'ID': stazione['ID']})
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
            dati=weatherData.find({'ID': stazione['ID']})
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
            dati=particulateData.find({'ID': stazione['ID']})
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



if __name__ == '__main__':
    app.run(debug = True, port= 5600)
    
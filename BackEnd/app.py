from io import BytesIO
from flask import Flask,jsonify,request,send_file,make_response,send_from_directory
import pandas as pd
from databases import particulateData,stations,weatherData,country
from tools import findCountry
import json
import pycountry
import datetime
from flask_cors import CORS
import requests
import re
from flask_compress import Compress



app = Flask(__name__)
CORS(app)
compress=Compress()
compress.init_app(app)

@app.route('/')
@compress.compressed()
def home():
    return "home"

@app.route("/getCountry")
@compress.compressed()
def getCountry():
    nazioni=country.find()
    array=[]
    for item in nazioni:
        del item['_id']
        if "latCountry" in item.keys():
            array.append(item)

    return jsonify(array)

@app.route("/getStationsByCountry")
@compress.compressed()
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
@compress.compressed()
def getAllStations():
    
    dati=stations.find() 
    array=[]
    for item in dati:
        del item['_id']
        array.append(item)
    return jsonify(array)

@app.route("/getDatafromCountry")
@compress.compressed()
def getDatafromCountry():
    country = request.args.get('country')
    if(country==""):
        return jsonify({"error" : "country non inserto"})
    time = request.args.get('time')
    if(time==""):
        return jsonify({"error" : "time non inserto"}) #day, week, month
    tipo = request.args.get('tipo')
    if(tipo==""):
        return jsonify({"error" : "tipo non inserto"}) #all, particulate, weather
    
    array=[]

    if tipo == 'particulate':
        if(time=="day"):
            now= datetime.datetime.now().date().strftime("%Y-%m-%d")    
            dati=particulateData.find({'country': country, 'timestamp': {'$regex': '^' + now}})
            for item in dati:
                del item['_id']
                array.append(item)
        elif(time=="week"):
            for i in range(7):
                countpm10=0
                countpm25=0
                cont=0
                now = (datetime.datetime.now() - datetime.timedelta(days=float(i))).strftime("%Y-%m-%d")
                    
                dati=particulateData.find({'country':country, 'timestamp': {'$regex': '^' + now}})
            
                for item in dati:
                    countpm10=countpm10 + item['pm10']
                    countpm25=countpm25 + item['pm2_5']
                    cont=cont+1
                if(cont >0):
                    dato ={'timestamp': now, 'pm10': countpm10/cont, 'pm2_5':countpm25/cont}
                    array.append(dato)
        elif(time=="month"):
            for i in range(30):
                countpm10=0
                countpm25=0
                cont=0

                now= (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
                dati=particulateData.find({'country':country, 'timestamp': {'$regex': '^' + now}})
            
                for item in dati:
                    countpm10=countpm10 + item['pm10']
                    countpm25=countpm25 + item['pm2_5']
                    cont=cont+1

                if(cont >0):
                    dato ={'timestamp': now, 'pm10': countpm10/cont, 'pm2_5':countpm25/cont}
                    array.append(dato)
    elif tipo == 'weather':
        if(time=="day"):
            now= datetime.datetime.now().date().strftime("%Y-%m-%d")    
            dati=weatherData.find({'country':country, 'timestamp': {'$regex': '^' + now}})
            for item in dati:
                del item['_id']
                array.append(item)
        elif(time=="week"):
            for i in range(7):
                counttemp=0
                counthum=0
                cont=0
                now= (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
                dati=weatherData.find({'country':country, 'timestamp': {'$regex': '^' + now}})
            
                for item in dati:
                    counttemp=counttemp + item['temperatura']
                    counthum=counthum + item['umidita']
                    cont=cont+1

                if(cont >0):
                    dato ={'timestamp': now, 'temperatura': counttemp/cont, 'umidita':counthum/cont}
                    array.append(dato)
        elif(time=="month"):
            for i in range(30):
                counttemp=0
                counthum=0
                cont=0
                now= (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
                dati=weatherData.find({'country':country, 'timestamp': {'$regex': '^' + now}})
            
                for item in dati:
                    counttemp=counttemp + item['temperatura']
                    counthum=counthum + item['umidita']
                    cont=cont+1

                if(cont >0):
                    dato ={'timestamp': now, 'temperatura': counttemp/cont, 'umidita':counthum/cont}
                    array.append(dato)
            
    if (len(array)>0):
        return jsonify(array)
    else:
        return jsonify({"error" : "Dati non trovati"})

@app.route("/getParticulateDataDayfromCountry")
@compress.compressed()
def getParticulateDataDayfromCountry():
    country = request.args.get('country')
    if(country==""):
        return jsonify({"error" : "country non inserto"})
    
    array=[]

    dati=particulateData.find({'country':country})
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
@compress.compressed()
def getWeatherDataDayfromCountry():
    country = request.args.get('country')
    if(country==""):
        return jsonify({"error" : "country non inserto"})
    
    array=[]
    
    dati=weatherData.find({'country':country})
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

@app.route("/CountSensorItaly")
@compress.compressed()
def CountSensorItaly():    
    dati=stations.count_documents({"country" : 'IT'}) 
    return jsonify({"dati":dati})

@app.route("/CountSensor")
@compress.compressed()
def CountSensor():    
    dati=stations.count_documents({}) 
    return jsonify({"dati":dati})

@app.route("/CountDataWorld")
@compress.compressed()
def CountDataWorld():    
    datipartculate=particulateData.count_documents({})
    datiweather=weatherData.count_documents({}) 
    return jsonify({"dati":datipartculate+datiweather})

@app.route("/download")
@compress.compressed()
def downlaod():
    country = request.args.get('country')
    if(country==""):
        return jsonify({"error" : "country non inserto"})
    time = request.args.get('time')
    if(time==""):
        return jsonify({"error" : "time non inserto"}) #day, week, month, custom
    if(time=="custom"):    
        datainizio = request.args.get('datainizio')
        if(datainizio==""):
            return jsonify({"error" : "datainizio non inserto"})
        datafine = request.args.get('datafine')
        if(datafine==""):
            return jsonify({"error" : "datafine non inserto"})
    tipo = request.args.get('tipo')
    if(tipo==""):
        return jsonify({"error" : "tipo non inserto"}) #particulate, weather
    download = request.args.get('download')
    if(download==""):
        return jsonify({"error" : "download non inserto"}) #json, excel, csv
    array=[]

    
    if tipo == 'particulate':
        
        if(time == "day"):
            now= datetime.datetime.now().date().strftime("%Y-%m-%d")    
            dati=particulateData.find({'country':country, 'timestamp': {'$regex': '^' + now}})
            for item in dati:
                del item['_id']
                array.append(item)
        elif(time=="week"):
            for i in range(7):
                countpm10=0
                countpm25=0
                cont=0
                now= (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
                dati=particulateData.find({'country':country, 'timestamp': {'$regex': '^' + now}})
            
                for item in dati:
                    countpm10=countpm10 + item['pm10']
                    countpm25=countpm25 + item['pm2_5']
                    cont=cont+1

                if(cont >0):
                    dato ={'timestamp': now, 'pm10': countpm10/cont, 'pm2_5':countpm25/cont}
                    array.append(dato)
        elif(time=="month"):
            for i in range(30):
                countpm10=0
                countpm25=0
                cont=0
                now= (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
                dati=particulateData.find({'country':country, 'timestamp': {'$regex': '^' + now}})
            
                for item in dati:
                    countpm10=countpm10 + item['pm10']
                    countpm25=countpm25 + item['pm2_5']
                    cont=cont+1

                if(cont >0):
                    dato ={'timestamp': now, 'pm10': countpm10/cont, 'pm2_5':countpm25/cont}
                    array.append(dato)
        elif(time=="custom"):
            startdate=datetime.datetime.strptime(datainizio,"%Y-%m-%d")
            finishdate = datetime.datetime.strptime(datafine,"%Y-%m-%d")

            for i in (finishdate-startdate):
                countpm10=0
                countpm25=0
                cont=0
                now= (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
                dati=particulateData.find({'country':country, 'timestamp': {'$regex': '^' + now}})
            
                for item in dati:
                    countpm10=countpm10 + item['pm10']
                    countpm25=countpm25 + item['pm2_5']
                    cont=cont+1

                if(cont >0):
                    dato ={'timestamp': now, 'pm10': countpm10/cont, 'pm2_5':countpm25/cont}
                    array.append(dato)

    elif tipo == 'weather':
        if(time=="day"):
            now= datetime.datetime.now().date().strftime("%Y-%m-%d")    
            dati=weatherData.find({'country':country, 'timestamp': {'$regex': '^' + now}})
            for item in dati:
                del item['_id']
                array.append(item)
        elif(time=="week"):
            for i in range(7):
                counttemp=0
                counthum=0
                cont=0
                
                now= (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
                dati=weatherData.find({'country':country, 'timestamp': {'$regex': '^' + now}})
            
                for item in dati:
                    counttemp=counttemp + item['temperatura']
                    counthum=counthum + item['umidita']
                    cont=cont+1

                if(cont >0):
                    dato ={'timestamp': now, 'temperatura': counttemp/cont, 'umidita':counthum/cont}
                    array.append(dato)
        elif(time=="month"):
            for i in range(30):
                counttemp=0
                counthum=0
                cont=0
                now= (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
                dati=weatherData.find({'country':country, 'timestamp': {'$regex': '^' + now}})
            
                for item in dati:
                    counttemp=counttemp + item['temperatura']
                    counthum=counthum + item['umidita']
                    cont=cont+1

                if(cont >0):
                    dato ={'timestamp': now, 'temperatura': counttemp/cont, 'umidita':counthum/cont}
                    array.append(dato)
        elif(time=="custom"):
            startdate=datetime.datetime.strptime(datainizio,"%Y-%m-%d")
            finishdate = datetime.datetime.strptime(datafine,"%Y-%m-%d")

            for i in (finishdate-startdate):
                counttemp=0
                counthum=0
                cont=0
                now= (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
                dati=weatherData.find({'country':country, 'timestamp': {'$regex': '^' + now}})
            
                for item in dati:
                    counttemp=counttemp + item['temperatura']
                    counthum=counthum + item['umidita']
                    cont=cont+1

                if(cont >0):
                    dato ={'timestamp': now, 'temperatura': counttemp/cont, 'umidita':counthum/cont}
                    array.append(dato)

    pan= pd.DataFrame.from_dict(array)

    if download == "json":
        pan.to_json("download\example.json")
        return send_from_directory(directory="download", path="example.json", as_attachment=True)
    elif download == "csv":
        resp = make_response(pan.to_csv())
        resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp
    elif download == "excel":
        pan.to_excel("download\example.xlsx")
        return send_from_directory(directory="download", path="example.xlsx", as_attachment=True)

if __name__ == '__main__':
    app.run(debug = True, port= 5600)
    
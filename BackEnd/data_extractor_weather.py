import json
import requests
import datetime
from databases import weatherData,stations

r = requests.get("https://api.luftdaten.info/static/v2/data.temp.min.json")
dati = json.loads(r.text)

for pippo in dati:
    dictsData = {}
    dictsStation = {}

    for item in pippo['sensordatavalues']:
        if(item['value_type'] == 'humidity'):
            umidita = float(item['value'])
        elif(item['value_type'] == 'temperature'):
            temperatura = float(item['value'])
    if (umidita > 0 or (temperatura > -30 and temperatura < 80)):
        if(pippo['location']['latitude'] !='' and  pippo['location']['longitude']):

            req = requests.get("https://nominatim.sensesquare.eu/nominatim/reverse?lat="+ str(pippo['location']['latitude']) +"&lon="+ str(pippo['location']['longitude']) +"&format=json&zoom=10")
        
            if "address" in req.json():
                georeq = req.json()['address']

                if "state" not in georeq.keys():
                    if "city" in georeq.keys():
                        dictsStation['regione'] = georeq['city']
                        dictsStation['provincia'] = georeq['city']
                        dictsStation['citta'] = georeq['city']
                else:
                    dictsStation['regione'] = georeq['state']
                if "county" in georeq.keys():
                    dictsStation['provincia'] = georeq['county']
                if "municipality" in georeq.keys():
                    dictsStation['citta'] = georeq['municipality']
                else:
                    if "city" in georeq.keys():
                        dictsStation['citta'] = georeq['city']
                    else:
                        if "town" in georeq.keys():
                            dictsStation['citta'] = georeq['town']
       
                dictsData['ID'] = 'SC' + str(pippo['id'])
                dictsStation['ID'] = 'SC' + str(pippo['id'])
                dictsData['timestamp'] = pippo['timestamp']
                dictsStation['latitude'] = float(pippo['location']['latitude'])
                dictsStation['longitude'] = float(pippo['location']['longitude'])
                dictsStation['country'] = pippo['location']['country']
                dictsStation['indoor'] = pippo['location']['indoor']
                dictsStation['weather'] = True
                dictsStation['particulate'] = False

                for item in pippo['sensordatavalues']:
                    if(item['value_type'] == 'humidity'):
                        dictsData['umidita'] = umidita
                    elif(item['value_type'] == 'temperature'):
                        dictsData['temperatura'] = temperatura
                try:
                    weatherData.insert_one(dictsData)
                except:
                    print("errore inserimento Weather")
            
                try:
                    cerco = stations.find_one({'ID': dictsStation['ID']})
                    if(cerco == None):
                        stations.insert_one(dictsStation)
                    else:
                        cerco['weather'] = True
                        stations.delete_one({"ID": cerco['ID']})
                        stations.insert_one(cerco)
                except:
                    print("errore inserimento Station")
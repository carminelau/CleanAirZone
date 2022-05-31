import requests
from databases import particulateData,stations,weatherData
import json

def deleteAll(name):
    for item in name.find():
        ide = item['_id']

        name.delete_one({'_id':ide})

def findCountry():
    lst=[]
    for item in stations.find():
        lst.append(item['country'])
    return list(dict.fromkeys(lst))

def updateStationGeo(item):
        req = requests.get("https://nominatim.sensesquare.eu/nominatim/reverse?lat="+ str(item['latitude']) +"&lon="+ str(item['longitude']) +"&format=json&zoom=10")
        
        if "address" in req.json():
            georeq = req.json()['address']

            if "state" not in georeq.keys():
                if "city" in georeq.keys():
                    item['regione'] = georeq['city']
                    item['provincia'] = georeq['city']
                    item['citta'] = georeq['city']
            else:
                item['regione'] = georeq['state']
            if "county" in georeq.keys():
                item['provincia'] = georeq['county']
            if "municipality" in georeq.keys():
                item['citta'] = georeq['municipality']
            else:
                if "city" in georeq.keys():
                    item['citta'] = georeq['city']
                else:
                    if "town" in georeq.keys():
                        item['citta'] = georeq['town']
            

            stations.delete_one({"ID":item['ID']})

            stations.insert_one(item)

#updateStationsGeo()
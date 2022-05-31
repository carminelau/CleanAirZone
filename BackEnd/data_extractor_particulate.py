import json
import requests
import datetime
from databases import particulateData,stations

r = requests.get("https://api.luftdaten.info/static/v2/data.dust.min.json")
dati = json.loads(r.text)

for pippo in dati:
    dictsDate = {}
    dictsStation = {}

    for item in pippo['sensordatavalues']:
        if(item['value_type'] == 'P1'):
            pm10 = float(item['value'])
        elif(item['value_type'] == 'P2'):
            pm25 = float(item['value'])
    if ((pm10 > 0 and pm10<300) or ( pm25 > 0 and pm25<300)):
        if (pippo['location']['latitude']!='' and pippo['location']['longitude']!=''):

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

                dictsDate['ID'] = 'SC' + str(pippo['id'])
                dictsStation['ID'] = 'SC' + str(pippo['id'])
                dictsDate['timestamp'] = pippo['timestamp']
                dictsStation['latitude'] = float(pippo['location']['latitude'])
                dictsStation['longitude'] = float(pippo['location']['longitude'])
                dictsStation['country'] = pippo['location']['country']
                dictsStation['indoor'] = pippo['location']['indoor']
                dictsStation['particulate'] = True
                dictsStation['weather'] = False

                for item in pippo['sensordatavalues']:
                    if(item['value_type'] == 'P1'):
                        dictsDate['pm10'] = pm10
                    elif(item['value_type'] == 'P2'):
                        dictsDate['pm2_5'] = pm25
                try:
                    particulateData.insert_one(dictsDate)
                except:
                    print("errore inserimento Particulate")
                
                try:
                    cerco= stations.find_one({'ID': dictsStation['ID']})
                    if(cerco ==  None):
                        stations.insert_one(dictsStation)
                    else:
                        cerco['particulate'] = True
                        stations.delete_one({"ID": cerco['ID']})
                        stations.insert_one(cerco)
                except:
                    print("errore inserimento Station")
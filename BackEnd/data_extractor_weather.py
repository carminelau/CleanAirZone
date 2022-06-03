import json
import requests
import datetime
from databases import weatherData,stations,country
import concurrent.futures
import pycountry


r = requests.get("https://api.luftdaten.info/static/v2/data.temp.min.json")
dati = json.loads(r.text)

def extract(pippo):
    dictsData = {}
    dictsStation = {}
    dictsCountry={}

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
       
                dictsData['ID'] = pippo['location']['id']
                dictsData['timestamp'] = pippo['timestamp']
                dictsStation['latitude'] = float(pippo['location']['latitude'])
                dictsStation['longitude'] = float(pippo['location']['longitude'])
                dictsStation['country'] = pippo['location']['country']
                dictsCountry['alpha_2'] = pippo['location']['country']
                req = requests.get("https://nominatim.sensesquare.eu/nominatim/search?country=" + str(pippo['location']['country']))
                js=req.json()
                if(len(js)>0):
                    dictsCountry['latCountry']= js[0]['lat']
                    dictsCountry['lonCountry']= js[0]['lon']
                dictsCountry["name"] = pycountry.countries.get(alpha_2=pippo['location']['country']).name

                dictsStation['indoor'] = pippo['location']['indoor']
                dictsStation['weather'] = True
                dictsStation['particulate'] = False
                dictsData['latitude'] = float(pippo['location']['latitude'])
                dictsData['longitude'] = float(pippo['location']['longitude'])

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
                    cerco = stations.find_one({'latitude': dictsStation['latitude'], 'longitude':dictsStation['longitude']})
                    if(cerco == None):
                        stations.insert_one(dictsStation)
                    else:
                        cerco['weather'] = True
                        stations.delete_one({'latitude': cerco['latitude'], 'longitude':cerco['longitude']})
                        stations.insert_one(cerco)
                except:
                    print("errore inserimento Station")
                
                try:
                    cerco = country.find_one({'alpha_2': pippo['location']['country']})
                    print(cerco)
                    if(cerco == None):
                        country.insert_one(dictsCountry)
                    else:
                        print('già inserito')
                except:
                    print("errore inserimento country")

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures=[]
    for pippo in dati:
        futures.append(executor.submit(extract,pippo))

for future in concurrent.futures.as_completed(futures):
    print('Completed')
    
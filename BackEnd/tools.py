from databases import particulateData,stations,weatherData

def deleteAll(name):
    for item in name.find():
        ide = item['_id']

        name.delete_one({'_id':ide})

deleteAll(stations)
deleteAll(particulateData)
deleteAll(weatherData)
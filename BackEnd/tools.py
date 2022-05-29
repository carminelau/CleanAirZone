from databases import particulateData,stations,weatherData

def deleteAll(name):
    for item in name.find():
        ide = item['_id']

        name.delete_one({'_id':ide})

def findCountry():
    lst=[]
    for item in stations.find():
        lst.append(item['country'])
    return list(dict.fromkeys(lst))

from tools import updateStationGeo, deleteAll
import concurrent.futures
from databases import stations,particulateData,weatherData,country

# with concurrent.futures.ThreadPoolExecutor() as executor:

#     futures=[]
#     for item in stations.find():
#         futures.append(executor.submit(updateStationGeo,item))

#     for future in concurrent.futures.as_completed(futures):
#         print('Completed')

deleteAll(stations)
deleteAll(particulateData)
deleteAll(weatherData)
deleteAll(country)
import datetime
from tools import updateStationGeo, deleteAll
import concurrent.futures
from databases import stations,particulateData,weatherData,country

# with concurrent.futures.ThreadPoolExecutor() as executor:

#     futures=[]
#     for item in stations.find():
#         futures.append(executor.submit(updateStationGeo,item))

#     for future in concurrent.futures.as_completed(futures):
#         print('Completed')

now= datetime.datetime.now().date().strftime("%Y-%m-%d")
query = { "timestamp": { "$regex": '^' + now } }
docs = particulateData.count_documents( query )

print(docs)
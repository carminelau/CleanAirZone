from tools import updateStationGeo
import concurrent.futures
from databases import stations

with concurrent.futures.ThreadPoolExecutor() as executor:

    futures=[]
    for item in stations.find():
        futures.append(executor.submit(updateStationGeo,item))

    for future in concurrent.futures.as_completed(futures):
        print('Completed')
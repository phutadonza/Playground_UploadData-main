#import pandas as pd
#
#path = r'C:\Users\Dell\Desktop\CCTV\Treading\CSV\CCTV-dt\CCTV-SYMC-RTC-13_148.csv'
#data = pd.read_csv(path)
#
#thing_list = []
#for stream in data['POLE_NAME']:
#    #stream_cut = stream.split("-")[:-1]
#    #thing_list.append("-".join(stream_cut))
#    
#    thing_list.append(stream)
#    
##print(thing_list)
#
#thing_list = list(dict.fromkeys(thing_list))
#print(f"Total Thing: {len(thing_list)}")

import requests
import json
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

import sys
import os

VALLARIS_API_KEY             = os.getenv("VALLARIS_API_KEY", "4fpxp8Qj8QmdhbHSTPCBHvzeF5avWVnfWIqRQQiYEoBzcVlLL2hnGZXa2VVdGLgp")
VALLARIS_URL                 = os.getenv("VALLARIS_URL", "https://app.larry-cctv.com/core/api")

datastreamID = "65b1021461f83a8dcaf0cb19"

url = f"{VALLARIS_URL}/streaming/v1.1/Datastreams({datastreamID})/Observations?$top=1"
# print(url)
payload = {}
headers = {
    'API-Key': VALLARIS_API_KEY
}

response = requests.request("GET", url, headers=headers, data=payload).json()


print(response)

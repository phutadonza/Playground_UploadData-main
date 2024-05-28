# %%
import requests
import json
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

import sys
import os
import dotenv
dotenv.load_dotenv()
VALLARIS_API_KEY             = os.getenv("VALLARIS_API_KEY", "4fpxp8Qj8QmdhbHSTPCBHvzeF5avWVnfWIqRQQiYEoBzcVlLL2hnGZXa2VVdGLgp")
VALLARIS_URL                 = os.getenv("VALLARIS_URL", "https://app.larry-cctv.com/core/api")


CAMERA_STATUS_OBSERVED_ID    = os.getenv("CAMERA_STATUS_OBSERVED_ID", "6502b538692d9156bfda65ef")
NVR_STATUS_OBSERVED_ID       = os.getenv("NVR_STATUS_OBSERVED_ID", "6502b553692d9156bfda65f1")
HDD_STATUS_OBSERVED_ID       = os.getenv("HDD_STATUS_OBSERVED_ID", "6502b545692d9156bfda65f0")

ObservedPropertyID_LIST = [CAMERA_STATUS_OBSERVED_ID,NVR_STATUS_OBSERVED_ID,HDD_STATUS_OBSERVED_ID]


# %%
def getZoneThing(zone : str):

    # url = f"{VALLARIS_URL}/streaming/v1.1/Things?$top=1000&$expand=Datastreams,Datastreams/ObservedProperty,Datastreams/Thing,Datastreams/Sensor&name={zone}-*"
    url = f"{VALLARIS_URL}/streaming/v1.1/Things?$top=1000&&name={zone}"
    # print(url)
    data = requests.get(url, headers={"API-Key": VALLARIS_API_KEY}).json()
    # print(data)
    return data

def getThingByName(zone : str):

    # url = f"{VALLARIS_URL}/streaming/v1.1/Things?$top=1000&$expand=Datastreams,Datastreams/ObservedProperty,Datastreams/Thing,Datastreams/Sensor&name={zone}-*"
    url = f"{VALLARIS_URL}/streaming/v1.1/Things?$top=1000&name={zone}&$expand=Datastreams,Datastreams/Sensor,Datastreams/Thing,Datastreams/ObservedProperty"
    # print(url)
    data = requests.get(url, headers={"API-Key": VALLARIS_API_KEY}).json()
    # print(data)
    return data


# %%
def getObservationByDAtastream(datastreamID : str):
    url = f"{VALLARIS_URL}/streaming/v1.1/Datastreams({datastreamID})/Observations?$top=1"
    # print(url)
    payload = {}
    headers = {
        'API-Key': VALLARIS_API_KEY
    }

    response = requests.request("GET", url, headers=headers, data=payload).json()

    return response

def getDatastreamByThing(thingID : str):
    url = f"{VALLARIS_URL}/streaming/v1.1/Things({thingID})/Datastreams?$top=1000&$expand=Sensor,Thing,ObservedProperty"
    # print(url)
    payload = {}
    headers = {
        'API-Key': VALLARIS_API_KEY
    }

    response = requests.request("GET", url, headers=headers, data=payload).json()

    return response


def getRTCList():
    url = f"http://10.94.12.211:1901/api/streams"
    data = requests.get(url).json()
    return data

RTC_LIST = getRTCList()

# %%
thing_list = []
for stream in RTC_LIST:
    stream_cut = stream.split("-")[:-1]
    # print("-".join(stream_cut))
    thing_list.append("-".join(stream_cut))

thing_list = list(dict.fromkeys(thing_list))
print(f"Total Thing: {len(thing_list)}")


# %%
def updateThing(thing_name):
    # print(thing_name)
    # print(getThingByName(thing_name))
    # thing = {}
    thing = getThingByName(thing_name)["value"]
    
    if (len(thing) == 0):
        return 0
    else:
        thing = thing[0]
    
    # if (len(thing["Datastreams"]) == 0):
    #     return 0
    
    # print(thing["Datastreams"])

    thing_properties = thing["properties"]

    thing_properties["name"] = thing["name"]
    try:
        thing_properties["district"] = thing["properties"]["district"]
    except:
        thing_properties["district"] = ""
        # print(thing["name"])
    # thing_properties["nvr_ip"] = thing["properties"]["nvr_ip"]
    if True :
        # print(thing["properties"])
    # thing_properties["nvr_ip"] != "":
        thing_properties["thing_iot_id"] = thing["@iot.id"]
        thing_properties["description"] = thing["description"]
        for ti in ObservedPropertyID_LIST:
            thing_properties[f"{ti}_total"] = 0
            thing_properties[f"{ti}_online"] = 0

        for datastream in thing["Datastreams"]:
            # print(datastream)
            try:
                LAT = datastream["Thing"]["properties"]["lat"]
                LON = datastream["Thing"]["properties"]["lon"]
            except:
                LAT = 0
                LON = 0
            ObservedPropertyID = datastream["ObservedProperty"]["@iot.id"]
            if (ObservedPropertyID in ObservedPropertyID_LIST):
                thing_properties[f"{ObservedPropertyID}_total"] += 1
                datastreamID = datastream["@iot.id"]
                try:
                    observation = getObservationByDAtastream(datastreamID)
                    if (observation["value"] != []):
                        if (observation["value"][0]["result"] == 1):
                            thing_properties[f"{ObservedPropertyID}_online"] += 1
                except:
                    pass

        try:
            thing_properties["camera_status"]   = int(thing_properties[f"{CAMERA_STATUS_OBSERVED_ID}_online"] / thing_properties[f"{CAMERA_STATUS_OBSERVED_ID}_total"])
        except:
            thing_properties["camera_status"]   = 0
        try:
            thing_properties["nvr_status"]      = int(thing_properties[f"{NVR_STATUS_OBSERVED_ID}_online"] / thing_properties[f"{NVR_STATUS_OBSERVED_ID}_total"])
        except:
            thing_properties["nvr_status"]      = 0
        try:
            thing_properties["hdd_status"]      = int(thing_properties[f"{HDD_STATUS_OBSERVED_ID}_online"] / thing_properties[f"{HDD_STATUS_OBSERVED_ID}_total"])
        except:
            thing_properties["hdd_status"]      = 0


    return 1
    
# %%
with tqdm(total=len(thing_list)) as pbar:
    with ThreadPoolExecutor(max_workers=32) as ex:
        futures = [ex.submit(updateThing, thing) for thing in thing_list]
        for future in as_completed(futures):
            result = future.result()

            
            
            







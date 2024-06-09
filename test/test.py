import requests
import json
import threading
import pandas as pd
from host.server import SERVER
from host.api import API
import read_js
import os


headers = {
            'API-Key':API,
            'Content-Type': 'application/json'      
        }


path = r'C:\Users\Dell\Desktop\CCTV\Treading\CSV\CCTV\13-24\CCTV-SYMC-RTC-13_148.csv'
 
       
def NVR():
    
    data = pd.read_csv(path)
    for j in range (len(data)):

        name = data._get_value(j,'POLE_NAME')

        #nvr = "6502b553692d9156bfda65f1"
        nvr = read_js.get_js("NVR-Status") # NVR-Statu
        
        url = f"{SERVER}/core/api/streaming/v1.1/ObservedProperties({nvr[0]})/Datastreams?&$expand=Sensor,Thing&$top=10000&name=*{name}*"
        #url = f"{SERVER}/core/api/streaming/v1.1/ObservedProperties({nvr[0]})/Datastreams?$top=10000&api_key={API}"
        res1 = requests.get(url=url,headers=headers).json()
        
        def InsertObsNVR(obs):
            
            url = f"{SERVER}/core/api/streaming/v1.1/Observations"
            payload = json.dumps({
                    "result" : 1,
                    "resultType": "number",
                    "Datastream":{"@iot.id":obs}
                }
            )
            response = requests.request("POST", url, headers=headers, data=payload)
            print(response)

        i = 0
        for obs in res1["value"]:
            InsertObsNVR(obs["@iot.id"])
            name = obs["name"]
            i += 1
            print(name,"NVR",i)

def Hard_Disk():
    data = pd.read_csv(path)
    for j in range (len(data)):

        name = data._get_value(j,'POLE_NAME')
        #disk = "6502b545692d9156bfda65f0"
        disk = read_js.get_js("Hard-Disk-Status") #RTSP-Live
        url = f"{SERVER}/core/api/streaming/v1.1/ObservedProperties({disk[0]})/Datastreams?&$expand=Sensor,Thing&$top=10000&name=*{name}*"
        #url = f"{SERVER}/core/api/streaming/v1.1/ObservedProperties({disk[0]})/Datastreams?$top=10000&api_key={API}"
        res1 = requests.get(url=url,headers=headers).json()
        
        def InsertObsHD(obs):
        
            url = f"{SERVER}/core/api/streaming/v1.1/Observations"
            payload = json.dumps({
                    "result" : 1,
                    "resultType": "number",
                    "Datastream":{"@iot.id":obs}
                }
            )
            response = requests.request("POST", url, headers=headers, data=payload)
            print(response)

        i = 0
        for obs in res1["value"]:
            InsertObsHD(obs["@iot.id"])
            name = obs["name"]
            i += 1
            print(name,"Hard_Disk",i)
        
def Camera():
    data = pd.read_csv(path)
    for j in range (len(data)):

        name = data._get_value(j,'POLE_NAME')
        #camera = "6502b538692d9156bfda65ef"
        camera = read_js.get_js("Camera-Status")
        url = f"{SERVER}/core/api/streaming/v1.1/ObservedProperties({camera[0]})/Datastreams?&$expand=Sensor,Thing&$top=10000&name=*{name}*"
        #url = f"{SERVER}/core/api/streaming/v1.1/ObservedProperties({camera[0]})/Datastreams?$top=10000&api_key={API}"
        res1 = requests.get(url=url,headers=headers).json()
        
        def InsertObsCM(obs):
        
            url = f"{SERVER}/core/api/streaming/v1.1/Observations"
            payload = json.dumps({
                    "result" : 1,
                    "resultType": "number",
                    "Datastream":{"@iot.id":obs}
                }
            )
            response = requests.request("POST", url, headers=headers, data=payload)
            print(response,)

        i = 0
        for obs in res1["value"]:
            InsertObsCM(obs["@iot.id"])
            name = obs["name"]
            i += 1
            print(name,"Camera",i)


# สร้าง Thread สำหรับแต่ละฟังก์ชัน
thread1 = threading.Thread(target=NVR)
thread2 = threading.Thread(target=Hard_Disk)
thread3 = threading.Thread(target=Camera)

# เริ่มการทำงานของแต่ละ Thread
thread1.start()
thread2.start()
thread3.start()

# รอให้ทั้งสอง Thread ทำงานเสร็จ
thread1.join()
thread2.join()
thread3.join()

print("ทำงานเสร็จสิ้น")




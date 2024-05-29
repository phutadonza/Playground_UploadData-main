import requests
import json
import threading
import pandas as pd
from host.server import SERVER
from host.api import API
import read_js
import os




# def Live():
    
#     file= "Camera-SB-list.csv"
#     filter = file.split("-")
#     data = pd.read_csv(r"Camera-SB-list.csv")
#     live = read_js.get_js("RTSP-Live") #RTSP-Live 

#     url = f"{SERVER}/core/api/streaming/v1.1/ObservedProperties({live[0]})/Datastreams?&$expand=Sensor,Thing&$top=10000&name=*{filter[1]}*"
    
#     response = requests.get(url,headers=headers)
#     response_json = response.json()

#     print(response_json["@iot.count"])

#     for i in  range (len(response_json["value"])):
#         for j in range (len(data)):
#             if response_json["value"][i]["Sensor"]["name"] == data._get_value(j,'CAMERA_NAME'): 
#                 while True:
#                     datastream = response_json["value"][i]["@iot.id"]
#                     # datastream = data._get_value(j,'POLE_NAME')
#                     name = response_json["value"][i]["Sensor"]["name"]
#                     port = data._get_value(j,'RTC_PORT')
#                     ip = data._get_value(j,'RTC_IP')
#                     #print(i,response_json["value"][i]["name"],ip,port)

#                     link = f"http://{ip}:{port}/api/stream.m3u8?src={name}mp4=flac"

                        
#                     payload = json.dumps({
#                     "result" : link,
#                     "resultType": "string",
#                     "Datastream":{"@iot.id":datastream},
#                     })
#                     url_post = "https://cctv2.naimueang.com/core/api/streaming/v1.1/Observations"
#                     response = requests.request("POST", url_post, headers=headers, data=payload)

#                     print(i,live[1],link,"//",response.status_code)

#                     if response.status_code == 201:
#                         break

headers = {
            'API-Key':API,
            'Content-Type': 'application/json'      
        }
       
def NVR():
    #nvr = "6502b553692d9156bfda65f1"
    nvr = read_js.get_js("NVR-Status") # NVR-Statu
    url = f"{SERVER}/core/api/streaming/v1.1/ObservedProperties({nvr[0]})/Datastreams?$top=10000"
    res1 = requests.get(url,headers=headers).json()
    
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
        i += 1
        print("NVR",i)

def Hard_Disk():
    #disk = "6502b545692d9156bfda65f0"
    disk = read_js.get_js("Hard-Disk-Status") #RTSP-Live
    url = f"{SERVER}/core/api/streaming/v1.1/ObservedProperties({disk[0]})/Datastreams?$top=10000"
    res1 = requests.get(url,headers=headers).json()
    
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
        i += 1
        print("Hard_Disk",i)
        
def Camera():
    #camera = "6502b538692d9156bfda65ef"
    camera = read_js.get_js("Camera-Status")
    url = f"{SERVER}/core/api/streaming/v1.1/ObservedProperties({camera[0]})/Datastreams?$top=10000"
    res1 = requests.get(url,headers=headers).json()
    
    def InsertObsCM(obs):
    
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
        InsertObsCM(obs["@iot.id"])
        i += 1
        print("Camera",i)


def Insert_status():

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

Insert_status()



import requests
import pandas as pd
import json
from host.server import SERVER
from host.api import API
import os


# dir_path = r'C:\Users\phuta\Desktop\Playground_UploadData-main\CSV - larry1\CCTV-out-dt'  #for edit at home

dir_path = r'C:\Users\phutadon\OneDrive\Desktop\Playground_UploadData-main\CSV - larry1\CCTV-out-dt'


for path in os.listdir(dir_path):  #path
    if os.path.isfile(os.path.join(dir_path, path)):
        print(os.path.join(dir_path, path))
        data = pd.read_csv( os.path.join(dir_path, path)) 

        url = f"{SERVER}/core/api/streaming/v1.1/Observations"

        headers = {
        'Content-Type': 'application/json',
        'API-Key':API
        }
            
        for i in range (len(data)):
            datastream = data._get_value(i,'DATASTREAM_ID (Live)')
            name = data._get_value(i,'CAMERA_NAME')
            # pole_name = data._get_value(i,'POLE_NAME')
            # description = data._get_value(i,'POLE_DESCRIPTION')
            port = data._get_value(i,'RTC_PORT')
            ip = data._get_value(i,'RTC_IP')
            # lon = data._get_value(i,'LON')
            # lat = data._get_value(i,'LAT')
            
            link = f"http://{ip}:{port}/api/stream.m3u8?src={name}&mp4=flac" ## create link for play in vlc
            
            print(i,link)
            
            payload = json.dumps({
            "result" : link,
            "resultType": "string",
            "Datastream":{"@iot.id":datastream}
            })
            response = requests.request("POST", url, headers=headers, data=payload)
            
            print(response)
            print (link)



import requests
import pandas as pd
import json
from host.server import SERVER
from host.api import API
import os

dir_path = r'C:\Users\phuta\Desktop\Playground_UploadData-main\CSV - larry1\CCTV-out-dt'  #for edit at home

for path in os.listdir(dir_path):  #path
    if os.path.isfile(os.path.join(dir_path, path)):
        print(os.path.join(dir_path, path))
        data = pd.read_csv(os.path.join(dir_path, path)) 

        url = f"{SERVER}/core/api/streaming/v1.1/Observations"

        headers = {
            'Content-Type': 'application/json',
            'API-Key': API
        }
        
        for i in range(len(data)):
            datastream = data._get_value(i, 'DATASTREAM_ID (Live)')
            name = data._get_value(i, 'CAMERA_NAME')
            rtc_zone = data._get_value(i, 'RTC_ZONE')
            
            link = f"https://{rtc_zone}/api/stream.mp4?src={name}&mp4=flac"  ## create link for play in vlc
            print(i, link)
            
            payload = json.dumps({
                "result": link,
                "resultType": "string",
                "Datastream": {"@iot.id": datastream}
            })
            
            response = requests.request("POST", url, headers=headers, data=payload)
            
            print(response)
            print(link)

print("Operation completed")

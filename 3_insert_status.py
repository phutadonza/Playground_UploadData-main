import pandas as pd
import requests
import json
import os
from host.server import SERVER
from host.api import API

# ฟังก์ชั่นสำหรับการโพสต์ข้อมูล
def post_observation(api_url, datastream_id, headers):
    url = f"{api_url}/Observations"
    payload = json.dumps({
        "result": 1,
        "resultType": "number",
        "Datastream": {"@iot.id": datastream_id}
    })
    response = requests.post(url, headers=headers, data=payload)
    # print(response.status_code, response.text)

# อ่านไฟล์ CSV
directory = r"C:\Users\phutadon\OneDrive\Desktop\Playground_UploadData-main\CSV - larry1\CCTV-out-dt"  # ระบุ path ไปยังไดเรกทอรี่ที่เก็บไฟล์ CSV
api_base_url = f"{SERVER}/core/api/streaming/v1.1"
headers = {
    'Content-Type': 'application/json',
    'API-Key': f'{API}'  # แทนที่ด้วย token ของคุณ
}

for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        filepath = os.path.join(directory, filename)
        df = pd.read_csv(filepath)
        
        for index, row in df.iterrows():
            camera_name = row['CAMERA_NAME']
            api_url = f"{api_base_url}/Sensors?name={camera_name}*"

            # เรียก API เพื่อดึงข้อมูล Sensor
            sensor_response = requests.get(api_url, headers=headers)
            if sensor_response.status_code == 200:
                print(f"Successfully fetched sensor data for {camera_name}")
                sensor_data = sensor_response.json()
                if sensor_data["@iot.count"] > 0:
                    datastream_link = sensor_data["value"][0]["Datastreams@iot.navigationLink"]
                    
                    # เรียก API เพื่อดึงข้อมูล Datastreams
                    datastream_response = requests.get(datastream_link, headers=headers)
                    if datastream_response.status_code == 200:
                        print(f"Successfully fetched datastream data for {camera_name}")
                        datastream_data = datastream_response.json()
                        
                        for datastream in datastream_data["value"]:
                            datastream_name = datastream["name"]
                            if "NVR-Status" in datastream_name or "Hard-Disk-Status" in datastream_name or "Camera-Status" in datastream_name:
                                datastream_id = datastream["@iot.id"]
                                print(f"Posting observation for Datastream ID: {datastream_id} with name: {datastream_name}")
                                post_observation(api_base_url, datastream_id, headers)
                            # else:
                            #     print(f"Not a matching Datastream: {datastream_name}")
                    else:
                        print(f"Error fetching datastream data for {camera_name}: {datastream_response.status_code} - {datastream_response.text}")
                else:
                    print(f"No sensor data found for {camera_name}")
            else:
                print(f"Error fetching sensor data for {camera_name}: {sensor_response.status_code} - {sensor_response.text}")

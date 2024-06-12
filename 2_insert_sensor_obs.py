import csv
import requests
import json
import pandas as pd
import threading
from dotenv import load_dotenv
import os

# โหลดค่า environment variables จากไฟล์ .env
load_dotenv()

# อ่านค่า environment variables
API_test = os.getenv('API_TEST')
SERVER_test = os.getenv('SERVER_TEST')

# ตรวจสอบว่า SERVER_test และ API_test ไม่เป็น None
if not SERVER_test or not API_test:
    raise ValueError("SERVER_URL_TEST หรือ API_KEY_TEST ไม่ได้ถูกตั้งค่าในไฟล์ .env")

def get_existing_sensors(headers):
    url = f"{SERVER_test}/core/api/streaming/v1.1/Sensors"
    params = {
        '$select': 'name',
        '$top': 10000  # ปรับตามที่จำเป็นเพื่อดึงข้อมูลทั้งหมด
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        sensors = response.json()
        return [sensor['name'] for sensor in sensors['value']]
    else:
        print("Error fetching sensors: %s" % response.text)
        return []

def createSensor(cctvDetail, headers):
    url = f"{SERVER_test}/core/api/streaming/v1.1/Sensors"
    payload = json.dumps({
        "name": cctvDetail["CAMERA_NAME"],
        "description": cctvDetail["CAMERA_DESCRIPTION"],
        "encodingType": "-",
        "metadata": "-",
        "properties": {
            "district": cctvDetail["DISTRICT"],
            "nvr_id": cctvDetail["POLE_NAME"],
            "nvr_ip": cctvDetail["NVR_IP"],
            "nvr_port": cctvDetail["NVR_PORT"],
            "nvr_channel_id": cctvDetail["NVR_CHANNEL_ID"],
            "nvr_brand": cctvDetail["NVR"],
            "nvr_api_type": cctvDetail["API"],
            "nvr_monitor_type": cctvDetail["MONITORING_TYPE"],
            "nvr_username": cctvDetail["NVR_USERNAME"],
            "nvr_password": cctvDetail["NVR_PASSWORD"]
        }
    })

    while True:
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 201:
            print("success with 201")
            break
        else:
            print("error occurred: %s" % response.text, " ", response.json())
            continue 

    res_json = response.json()
    return res_json["@iot.id"]

def createDatastream(dtDetail, headers):
    url = f"{SERVER_test}/core/api/streaming/v1.1/Datastreams"

    name = str(dtDetail["ThingName"]) + ":" + str(dtDetail["PropertyName"])
    uomName = "-"
    uomSymbol = "-"
    if "RTSP-Live" in dtDetail["PropertyName"]:
        uomName = "Live"
        uomSymbol = "hls"
    elif "ISAPI-Playback" in dtDetail["PropertyName"]:
        uomName = "ISAPI-Playback"
        uomSymbol = "hls"
    elif "DAHUA-API-Playback" in dtDetail["PropertyName"]:
        uomName = "DAHUA-API-Playback"
        uomSymbol = "hls"
    elif "Camera-Status" in dtDetail["PropertyName"]:
        uomName = "Camera-Status"
        uomSymbol = "bool"
    elif "Hard-Disk-Status" in dtDetail["PropertyName"]:
        uomName = "Hard-Disk-Status"
        uomSymbol = "bool"
    elif "NVR-Status" in dtDetail["PropertyName"]:
        uomName = "NVR-Status"
        uomSymbol = "bool"

    payload = json.dumps({
        "name": name,
        "description": "The datastream of " + name,
        "observationType": "-",
        "unitOfMeasurement": {
            "name": uomName,
            "symbol": uomSymbol,
            "definition": "-"
        },
        "Thing": {
            "@iot.id": dtDetail["ThingId"]
        },
        "ObservedProperty": {
            "@iot.id": dtDetail["PropertyId"]
        },
        "Sensor": {
            "@iot.id": dtDetail["SensorId"]
        }
    })

    while True:
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 201:
            print("success with 201")
            break
        else:
            print("error occurred: %s" % response.text, " ", response.json())
            continue 

    res_json = response.json()
    return res_json["@iot.id"]

dir_path = r'C:\Users\phutadon\OneDrive\Desktop\Playground_UploadData-main\CSV - larry1\CCTV-out' 
dir_json = r'C:\Users\phutadon\OneDrive\Desktop\Playground_UploadData-main\cctv2-observedProp.json'

headers = {
    'API-Key': API_test,
    'Content-Type': 'application/json'
}

def Insert_sensor():
    existing_sensors = get_existing_sensors(headers)

    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            print(os.path.join(dir_path, path))

            out_dict = []
            with open(dir_json, encoding='utf-8') as f:
                props = json.load(f)
            with open(os.path.join(dir_path, path), encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                num_row = 1
                dt_count = 0
                for row in csv_reader:
                    if row["LOCATION_ID"] and row["THING_ID"] and row["FEATUREOFINTEREST_ID"]:
                        if row["CAMERA_NAME"] not in existing_sensors:
                            print("num_row = %d" % num_row)
                            print("sensor = %s" % row["CAMERA_NAME"])
                            sensorId = createSensor(row, headers)
                            row["SENSOR_ID"] = sensorId

                            for p in props["value"]:
                                dtDetail = {
                                    "ThingName": row["POLE_NAME"],
                                    "ThingId": row["THING_ID"],
                                    "SensorId": sensorId,
                                    "PropertyId": p["@iot.id"],
                                    "PropertyName": p["name"]
                                }
                                datastreamId = createDatastream(dtDetail, headers)
                                if "Live" in p["name"]:
                                    row["DATASTREAM_ID (Live)"] = datastreamId
                                    out_dict.append(row)
                                
                                dt_count += 1

                            num_row += 1
                        else:
                            print(f"Duplicate sensor found: {row['CAMERA_NAME']}")
                    else:
                        print(f"Missing LOCATION_ID, THING_ID, or FEATUREOFINTEREST_ID in row {num_row}")

                print("-------- dt_count = %d" % dt_count)
            
            if out_dict:
                field_names = list(out_dict[0].keys())

                split_txt = os.path.join(dir_path, path).split('\\')
                name_text = split_txt[-1].split('.')
                file_save = f'C:\\Users\\phutadon\\OneDrive\\Desktop\\Playground_UploadData-main\\CSV - larry1\\CCTV-out-dt\\{name_text[0]}-dt.csv'

                with open(file_save, 'w', encoding='utf-8') as csvfile:      
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerows(out_dict)

thread1 = threading.Thread(target=Insert_sensor)

thread1.start()

thread1.join()

print("ทำงานเสร็จสิ้น")

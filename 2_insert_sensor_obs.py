import requests
import json
import csv
import os
import threading

SERVER = "https://yourserver.com"
API = "your_api_key"
headers = {
    'API-Key': API,
    'Content-Type': 'application/json'
}

dir_path = r'C:\Users\phutadon\OneDrive\Desktop\Playground_UploadData-main\CSV - larry1\CCTV-out'
dir_json = r'C:\Users\phutadon\OneDrive\Desktop\Playground_UploadData-main\cctv2-observedProp.json'

def checkThingExists(pole_name, headers, session):
    url = f"{SERVER}/core/api/streaming/v1.1/Things?$filter=name eq '{pole_name}'"
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        things = response.json()["value"]
        if things:
            return things[0]["@iot.id"]
    return None

def checkSensorExists(cctvDetail, headers, session):
    url = f"{SERVER}/core/api/streaming/v1.1/Sensors?$filter=name eq '{cctvDetail['CAMERA_NAME']}'"
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        sensors = response.json()["value"]
        if sensors:
            return sensors[0]["@iot.id"]
    return None

def createSensor(cctvDetail, headers, session):
    existingSensorId = checkSensorExists(cctvDetail, headers, session)
    if existingSensorId:
        print(f"Sensor already exists: {existingSensorId}")
        return existingSensorId

    url = f"{SERVER}/core/api/streaming/v1.1/Sensors"
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
        response = session.post(url, headers=headers, data=payload)
        if response.status_code == 201:
            print("success with 201")
            break
        else:
            print("error occurred: %s" % response.text, " ", response.json())
            continue 

    res_json = response.json()
    return res_json["@iot.id"]

def checkDatastreamExists(dtDetail, headers, session):
    url = f"{SERVER}/core/api/streaming/v1.1/Datastreams?$filter=name eq '{dtDetail['ThingName']}:{dtDetail['PropertyName']}'"
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        datastreams = response.json()["value"]
        if datastreams:
            return datastreams[0]["@iot.id"]
    return None

def createDatastream(dtDetail, headers, session):
    existingDatastreamId = checkDatastreamExists(dtDetail, headers, session)
    if existingDatastreamId:
        print(f"Datastream already exists: {existingDatastreamId}")
        return existingDatastreamId

    url = f"{SERVER}/core/api/streaming/v1.1/Datastreams"
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
        response = session.post(url, headers=headers, data=payload)
        if response.status_code == 201:
            print("success with 201")
            break
        else:
            print("error occurred: %s" % response.text, " ", response.json())
            continue 

    res_json = response.json()
    return res_json["@iot.id"]

def Insert_sensor():
    with requests.Session() as session:
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
                        print("num_row = %d" % num_row)
                        pole_id = checkThingExists(row["POLE_NAME"], headers, session)
                        if not pole_id:
                            print(f"Thing (POLE) not found: {row['POLE_NAME']}")
                            continue
                        
                        sensorId = createSensor(row, headers, session)
                        row["SENSOR_ID"] = sensorId
                        for p in props["value"]:
                            dtDetail = {
                                "ThingName": row["POLE_NAME"],
                                "ThingId": pole_id,
                                "SensorId": sensorId,
                                "PropertyId": p["@iot.id"],
                                "PropertyName": p["name"]
                            }
                            datastreamId = createDatastream(dtDetail, headers, session)
                            if "Live" in p["name"]:
                                row["DATASTREAM_ID (Live)"] = datastreamId
                                out_dict.append(row)
                            dt_count += 1
                        num_row += 1
                    print("-------- dt_count = %d" % dt_count)
                field_names = list(out_dict[0].keys())
                split_txt = os.path.join(dir_path, path).split('\\')
                name_text = split_txt[-1].split('.')
                file_save = f'C:\\Users\\phutadon\\OneDrive\\Desktop\\Playground_UploadData-main\\CSV - larry1\\CCTV-out-dt\\{name_text[0]}-dt.csv'
                with open(file_save, 'w', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerows(out_dict)

# สร้าง Thread สำหรับแต่ละฟังก์ชัน
thread1 = threading.Thread(target=Insert_sensor)

# เริ่มการทำงานของแต่ละ Thread
thread1.start()

# รอให้ทั้งสอง Thread ทำงานเสร็จ
thread1.join()

print("ทำงานเสร็จสิ้น")

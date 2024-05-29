import csv
import requests
import json
import pandas as pd
import threading
from host.server import SERVER
from host.api import API
import os
from insert_status_treading import Insert_status

def createSensor(cctvDetail,headers):
    
    url = f"{SERVER}/core/api/streaming/v1.1/Sensors"
    #url = "https://cctv2.naimueang.com/core/api/streaming/v1.1/Sensors"

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
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 201:
            print("success with 201")
            break
        else:
            print("error occurred: %s" % response.text," ",response.json())
            continue 

    res_json = response.json()
    return res_json["@iot.id"]

def createDatastream(dtDetail,headers):
    url = f"{SERVER}/core/api/streaming/v1.1/Datastreams"
    #url = "https://cctv2.naimueang.com/core/api/streaming/v1.1/Datastreams"

    name = str(dtDetail["ThingName"])+":"+str(dtDetail["PropertyName"])
    uomName ="-"
    uomSymbol = "-"
    if (str.__contains__(dtDetail["PropertyName"], "RTSP-Live")):
        uomName = "Live"
        uomSymbol = "hls"
    elif (str.__contains__(dtDetail["PropertyName"], "ISAPI-Playback")):
        uomName = "ISAPI-Playback"
        uomSymbol = "hls"
    elif (str.__contains__(dtDetail["PropertyName"], "DAHUA-API-Playback")):
        uomName = "DAHUA-API-Playback"
        uomSymbol = "hls"
    elif (str.__contains__(dtDetail["PropertyName"], "Camera-Status")):
        uomName = "Camera-Status"
        uomSymbol = "bool"
    elif (str.__contains__(dtDetail["PropertyName"], "Hard-Disk-Status")):
        uomName = "Hard-Disk-Status"
        uomSymbol = "bool"
    elif (str.__contains__(dtDetail["PropertyName"], "NVR-Status")):
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
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 201:
            print("success with 201")
            break
        else:
            print("error occurred: %s" % response.text," ",response.json())
            continue 

    res_json = response.json()
    return res_json["@iot.id"]


# dir_path = r'C:\Users\phuta\Desktop\Playground_UploadData-main\CSV - larry1\CCTV-out' # for edit at home
# dir_json = r'C:\Users\phuta\Desktop\Playground_UploadData-main\cctv2-observedProp.json' # for edit at home


dir_path = r'C:\Users\phutadon\OneDrive\Desktop\Playground_UploadData-main\CSV - larry1\CCTV-out' ##
dir_json = r'C:\Users\phutadon\OneDrive\Desktop\Playground_UploadData-main\cctv2-observedProp.json' ##

headers = {
    'API-Key': API,
    'Content-Type': 'application/json'
    }

def Insert_sensor():

    for path in os.listdir(dir_path):  #path
        if os.path.isfile(os.path.join(dir_path, path)):
            print(os.path.join(dir_path, path))

            out_dict = []
            f = open( dir_json , encoding='utf-8')
            props = json.load(f)
            with open(os.path.join(dir_path, path), encoding='utf-8') as csv_file:        ### Succes
                csv_reader = csv.DictReader(csv_file)
                num_row = 1
                dt_count = 0
                for row in csv_reader:
                    print("num_row = %d" % num_row)
                    print("sensor = %s" % row["CAMERA_NAME"])
                    # print("----- row = ",row)
                    # break
                    # create sensor
                    sensorId = createSensor(row,headers)
                    row["SENSOR_ID"] = sensorId
                    
                    for p in props["value"]:
                        dtDetail = {
                            "ThingName": row["POLE_NAME"],
                            "ThingId": row["THING_ID"],
                            "SensorId": sensorId,
                            "PropertyId": p["@iot.id"],
                            "PropertyName": p["name"]
                        }
                        # loop create datastream
                        datastreamId = createDatastream(dtDetail,headers)
                        if "Live" in p["name"]:
                            row["DATASTREAM_ID (Live)"] = datastreamId
                            out_dict.append(row)
                            
                        dt_count += 1

                    num_row += 1
                        
                    # break  ## for one camera

                print("-------- dt_count = %d" % dt_count)
            field_names = list(out_dict[0].keys())

            split_txt = os.path.join(dir_path, path).split('\\')
            name_text = split_txt[-1].split('.')
            #print(name_text)
            # file_save = f'C:\\Users\\phuta\\Desktop\\Playground_UploadData-main\\CSV - larry1\\CCTV-out-dt\\{name_text[0]}-dt.csv' ## for edit at home
            file_save = f'C:\\Users\\phutadon\\OneDrive\\Desktop\\Playground_UploadData-main\\CSV - larry1\\CCTV-out-dt\\{name_text[0]}-dt.csv' ##

            with open(file_save, 'w', encoding='utf-8') as csvfile:      
                writer = csv.DictWriter(csvfile, fieldnames = field_names)
                writer.writeheader()
                writer.writerows(out_dict)
    


# สร้าง Thread สำหรับแต่ละฟังก์ชัน
thread1 = threading.Thread(target=Insert_sensor)

# เริ่มการทำงานของแต่ละ Thread
thread1.start()

# รอให้ทั้งสอง Thread ทำงานเสร็จ
thread1.join()

print("ทำงานเสร็จสิ้น")


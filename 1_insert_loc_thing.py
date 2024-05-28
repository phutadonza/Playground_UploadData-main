import csv
import requests
import json
import threading
from host.server import SERVER
from host.api import API
import os
#from insert_sensor_obs  import Insert_obs

# Set Server in File host

def createLocation(cctvDetail, headers):
    url = f"{SERVER}/core/api/streaming/v1.1/Locations"

    payload = json.dumps({
    "name": str(cctvDetail["POLE_NAME"]),
    "description": str(cctvDetail["POLE_DESCRIPTION"]),
    "encodingType": "application/vnd.geo+json",
    "location": {
        "type": "Point",
        "coordinates": [
        float(cctvDetail["LON"]),
        float(cctvDetail["LAT"])
        ]
    }
    })
    while True:
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 201:
            print("success with 201")
            break
        else:
            print("error occurred: %s" % response.text,response.json())
            continue 
    res_json = response.json()
    cctvDetail["LOCATION_ID"] = res_json["@iot.id"]
    return cctvDetail

def createThing(cctvDetail, location_id , headers):
    url = f"{SERVER}/core/api/streaming/v1.1/Things"

    payload = json.dumps({
    "name": str(cctvDetail["POLE_NAME"]),
    "description": str(cctvDetail["POLE_DESCRIPTION"]),
    "properties": {
        "lat": float(cctvDetail["LAT"]),
        "lon": float(cctvDetail["LON"])
    },
    "Locations": [
        {
            "@iot.id": location_id
        }
    ]
    })

    print("----- json =", payload)
    while True:
        response = requests.request("POST", url, headers=headers, data=payload)
        # print(response.text)
        if response.status_code == 201:
            print("success with 201")
            break
        else:
            print("error occurred: %s" % response.text,response.json())
            continue
    res_json = response.json()
    cctvDetail["THING_ID"] = res_json["@iot.id"]
    return cctvDetail

def createFeatureOfInterest(cctvDetail , headers):
    url = f"{SERVER}/core/api/streaming/v1.1/FeaturesOfInterest"

    payload = json.dumps({
    "name": str(cctvDetail["POLE_NAME"]),
    "description": str(cctvDetail["POLE_DESCRIPTION"]),
    "encodingType": "application/vnd.geo+json",
    "feature": {
        "type": "Point",
        "coordinates": [
        float(cctvDetail["LON"]),
        float(cctvDetail["LAT"])
        ]
    }
    })
    while True:
        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 201:
            print("success with 201")
            break
        else:
            print("error occurred: %s" % response.text,response.json())
            continue

    res_json = response.json()
    print('vale form createFeatureOfInterest == ',res_json)
    cctvDetail["FEATUREOFINTEREST_ID"] = res_json["@iot.id"]

    return cctvDetail

# /////////////////////////////////
#dir_path = r'C:\\Users\\Administrator\\Desktop\\CCTV\\Treading\\CSV\\CCTV\\'

dir_path = r'C:\\Users\\phutadon\\OneDrive\\Desktop\\Playground_UploadData-main\\CSV - larry1\\CCTV'

headers = {
    'API-Key': API,
    'Content-Type': 'application/json'
    }

def Insert_pole():
    for path in os.listdir(dir_path):  #path
        if os.path.isfile(os.path.join(dir_path, path)):
            print('test',os.path.join(dir_path, path)) #ไว้เช็ค path

            out_dict = []   #CSV
            with open( os.path.join(dir_path, path) , encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                count = 0
                prev_name = ''
                locationid = ''
                thingid = ''
                featureid= ''
                # condition_column = 'thing.name / sensor.prop.nvr_id' 
                i = 1
                for row in csv_reader:
                    print("----- i =", i)
                    # print(row)
                    # break
                    
                    if row['POLE_NAME'] != prev_name:
                        prev_name = row['POLE_NAME']
            
                        
                        # print("----- row =", row)
                        # call create location
                        out = createLocation(row, headers)

                        # print("----- 1 out =", out)
                        locationid = out['LOCATION_ID']
                        # call create thing
                        
                        out = createThing(out, out['LOCATION_ID'], headers)

                        # print("----- 2 out =", out)
                        thingid = out["THING_ID"]
                        # call create featureOfOnterest
                        out = createFeatureOfInterest(out, headers)
                        
                        featureid = out["FEATUREOFINTEREST_ID"]

                        out_dict.append(out)
                        count += 1
                    else:
                        out_dict.append(row)      
                        out_dict[i-1]["LOCATION_ID"] = locationid           #
                        out_dict[i-1]["THING_ID"] = thingid                 #
                        out_dict[i-1]["FEATUREOFINTEREST_ID"] = featureid   #
                        
                    i = i+1
                    
                    # break  ## Test one camera
                
                print("-------- thing count = %d" % count) #run for end and show

            field_names = list(out_dict[0].keys())
            #-print( 'path', os.path.join(dir_path, path))
            split_txt = os.path.join(dir_path, path).split('\\')
            name_text = split_txt[-1].split('.')
            #-print( 'Split', split_txt)
            file_save = f'C:\\Users\\phutadon\\OneDrive\\Desktop\\Playground_UploadData-main\\CSV - larry1\\CCTV-out\\{name_text[0]}-out.csv'
            completeName  = os.path.join(file_save)
            #print('completeName  ',completeName)
            with open( completeName  , 'w' ,encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames = field_names)
                writer.writeheader()
                writer.writerows(out_dict)



# สร้าง Thread สำหรับแต่ละฟังก์ชัน
thread1 = threading.Thread(target=Insert_pole)

# เริ่มการทำงานของแต่ละ Thread
thread1.start()

# รอให้ทั้งสอง Thread ทำงานเสร็จ
thread1.join()

print("ทำงานเสร็จสิ้น")




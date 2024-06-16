import csv
import requests
import json
import threading
import os
import time
import pandas as pd
from dotenv import load_dotenv

# โหลดค่า environment variables จากไฟล์ .env
load_dotenv()

# อ่านค่า environment variables
API_REAL = os.getenv('API_REAL')
SERVER_REAL = os.getenv('SERVER_REAL')

print(SERVER_REAL, API_REAL)

# ตั้งค่าพารามิเตอร์พื้นฐาน
top = 10000
skip = 0
things_count = 10539
output_dir = r'C:\Users\phuta\Desktop\Playground_UploadData-main\CSV - larry1\CCTV-all'
output_file = os.path.join(output_dir, 'things_data.csv')
compare_dir = r'C:\Users\phuta\Desktop\Playground_UploadData-main\CSV - larry1\CCTV'
check_before_up_dir = r'C:\Users\phuta\Desktop\Playground_UploadData-main\CSV - larry1\CHECK BEFORE UP'
dir_path = r'C:\Users\phuta\Desktop\Playground_UploadData-main\CSV - larry1\CCTV'

# ตั้งค่า headers สำหรับ API
headers = {
    'API-Key': API_REAL,
    'Content-Type': 'application/json'
}

# ฟังก์ชันสำหรับดึงข้อมูลจาก API
def get_things_data(skip, top):
    url = f"{SERVER_REAL}/core/api/streaming/v1.1/Things?api_key={API_REAL}&$skip={skip}&$top={top}"
    response = requests.get(url)
    return response.json()

# ฟังก์ชันสำหรับดึงข้อมูล things และบันทึกลงไฟล์ CSV
def fetch_things_data():
    global skip
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['iot.id', 'name'])  # เขียน header

        while skip < things_count:
            data = get_things_data(skip, top)  # ดึงข้อมูลจาก API
            for item in data['value']:
                writer.writerow([item['@iot.id'], item['name']])
            skip += top

    print(f"Data has been written to {output_file}")

# ฟังก์ชันสำหรับตรวจสอบชื่อ POLE ที่ซ้ำกัน
def check_matching_names(things_df, compare_dir):
    matches = []

    # อ่านไฟล์ CSV ทั้งหมดในไดเรกทอรี compare_dir
    comparison_files = [f for f in os.listdir(compare_dir) if f.endswith('.csv')]

    for comp_file in comparison_files:
        comp_file_path = os.path.join(compare_dir, comp_file)
        comp_df = pd.read_csv(comp_file_path)

        # ตรวจสอบชื่อ POLE ที่ซ้ำกัน
        for thing_name in things_df['name']:
            if thing_name in comp_df['POLE_NAME'].values:
                matches.append((thing_name, comp_file))

    return matches

# ดึงข้อมูล things
fetch_things_data()

# อ่านข้อมูล things ที่ดึงมา
things_df = pd.read_csv(output_file)

# ตรวจสอบชื่อ POLE ที่ซ้ำกันและจัดการผลลัพธ์
matches = check_matching_names(things_df, compare_dir)

# บันทึกข้อมูลที่ซ้ำกันลงในไฟล์ CSV ในไดเรกทอรี CHECK BEFORE UP
if matches:
    match_file_path = os.path.join(check_before_up_dir, 'poleซ้ำกล้องไม่แอด.csv')
    with open(match_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['POLE_NAME', 'File'])  # เขียน header
        for match in matches:
            writer.writerow(match)
    print(f"Matches have been saved to {match_file_path}")

# ฟังก์ชันสำหรับสร้าง Location
def createLocation(cctvDetail, headers):
    url = f"{SERVER_REAL}/core/api/streaming/v1.1/Locations"
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
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            if response.status_code == 201:
                print("success with 201")
                break
            else:
                print("error occurred: %s" % response.text)
        except Exception as e:
            print(f"Exception occurred: {e}")

    res_json = response.json()
    cctvDetail["LOCATION_ID"] = res_json["@iot.id"]
    return cctvDetail

# ฟังก์ชันสำหรับสร้าง Thing
def createThing(cctvDetail, location_id , headers):
    url = f"{SERVER_REAL}/core/api/streaming/v1.1/Things"
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
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            if response.status_code == 201:
                print("success with 201")
                break
            else:
                print("error occurred: %s" % response.text)
        except Exception as e:
            print(f"Exception occurred: {e}")

    res_json = response.json()
    cctvDetail["THING_ID"] = res_json["@iot.id"]
    return cctvDetail

# ฟังก์ชันสำหรับสร้าง FeatureOfInterest
def createFeatureOfInterest(cctvDetail , headers):
    url = f"{SERVER_REAL}/core/api/streaming/v1.1/FeaturesOfInterest"
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
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            if (response.status_code == 201):
                print("success with 201")
                break
            else:
                print("error occurred: %s" % response.text)
        except Exception as e:
            print(f"Exception occurred: {e}")

    res_json = response.json()
    print('vale form createFeatureOfInterest == ', res_json)
    cctvDetail["FEATUREOFINTEREST_ID"] = res_json["@iot.id"]
    return cctvDetail

# ฟังก์ชันสำหรับเพิ่มข้อมูล POLE
def Insert_pole():
    pole_cache = {}
    pole_count = 0  # ตัวนับจำนวนเสาที่ถูกสร้างขึ้น

    for path in os.listdir(dir_path):  # path ของไฟล์ CSV
        if os.path.isfile(os.path.join(dir_path, path)):
            print('test', os.path.join(dir_path, path))  # ตรวจสอบ path

            split_txt = os.path.join(dir_path, path).split('\\')
            name_text = split_txt[-1].split('.')
            file_save = f'C:\\Users\\phuta\\Desktop\\Playground_UploadData-main\\CSV - larry1\\CCTV-out\\{name_text[0]}-out.csv'
            completeName = os.path.join(file_save)
            
            with open(completeName, 'w', encoding='utf-8', newline='') as output_csvfile:
                field_names = None
                writer = None
                
                with open(os.path.join(dir_path, path), encoding='utf-8') as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    count = 0
                    i = 1

                    # เตรียมตรวจสอบ POLE_NAME ที่ซ้ำกัน
                    rows = list(csv_reader)
                    for row in rows:
                        if row['POLE_NAME'] in things_df['name'].values:
                            pole_cache[row['POLE_NAME']] = {
                                "LOCATION_ID": "DUPLICATE",
                                "THING_ID": "DUPLICATE",
                                "FEATUREOFINTEREST_ID": "DUPLICATE"
                            }
                        elif row['POLE_NAME'] not in pole_cache:
                            # สร้าง location
                            out = createLocation(row, headers)
                            locationid = out['LOCATION_ID']

                            # สร้าง thing
                            out = createThing(out, locationid, headers)
                            thingid = out["THING_ID"]

                            # สร้าง feature of interest
                            out = createFeatureOfInterest(out, headers)
                            featureid = out["FEATUREOFINTEREST_ID"]

                            pole_cache[row['POLE_NAME']] = {
                                "LOCATION_ID": locationid,
                                "THING_ID": thingid,
                                "FEATUREOFINTEREST_ID": featureid
                            }
                            pole_count += 1  # เพิ่มตัวนับเมื่อสร้างเสาใหม่

                    for row in rows:
                        if row['POLE_NAME'] in pole_cache:
                            row.update(pole_cache[row['POLE_NAME']])

                        if field_names is None:
                            field_names = row.keys()
                            writer = csv.DictWriter(output_csvfile, fieldnames=field_names)
                            writer.writeheader()
                        
                        writer.writerow(row)
                        i += 1
                
                print("-------- thing count = %d" % count)  # แสดงจำนวน things

    # แสดงจำนวนเสาที่ถูกสร้างใน terminal
    print(f"Total Poles Created: {pole_count}")

# สร้าง Thread สำหรับฟังก์ชัน Insert_pole
thread1 = threading.Thread(target=Insert_pole)

# เริ่มการทำงานของ Thread
thread1.start()

# รอให้ Thread ทำงานเสร็จ
thread1.join()

print("ทำงานเสร็จสิ้น")

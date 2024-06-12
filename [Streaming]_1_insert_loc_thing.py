import csv
import requests
import json
import threading
import os
import time
import pandas as pd
from host.server import SERVER
from host.api import API

# ตั้งค่าพารามิเตอร์พื้นฐาน
top = 10000
skip = 0
things_count = 12000
output_dir = r'C:\Users\Demose\Desktop\luilayout\val\Playground_UploadData-main-main\Playground_UploadData-main-main\CSV - larry1\CCTV-all'
output_file = os.path.join(output_dir, 'things_data.csv')
compare_dir = r'C:\Users\Demose\Desktop\luilayout\val\Playground_UploadData-main-main\Playground_UploadData-main-main\CSV - larry1\CCTV'
check_before_up_dir = r'C:\Users\Demose\Desktop\luilayout\val\Playground_UploadData-main-main\Playground_UploadData-main-main\CSV - larry1\CHECK BEFORE UP'
dir_path = r'C:\Users\Demose\Desktop\luilayout\val\Playground_UploadData-main-main\Playground_UploadData-main-main\CSV - larry1\CCTV'

# ตั้งค่า headers สำหรับ API
headers = {
    'API-Key': API,
    'Content-Type': 'application/json'
}

# ฟังก์ชันสำหรับดึงข้อมูลจาก API
def get_things_data(skip, top):
    url = f"{SERVER}/core/api/streaming/v1.1/Things?api_key={API}&$skip={skip}&$top={top}"
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
            time.sleep(2)  # เพิ่มดีเลย์เป็น 2 วินาทีเพื่อลดโหลดเซิร์ฟเวอร์

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

# ฟังก์ชันสำหรับ retry request
def retry_request(func, args, kwargs, retries=2, timeout=30):
    attempt = 0
    while attempt < retries:
        try:
            response = func(*args, **kwargs, timeout=timeout)
            if response.status_code == 201:
                return response
            else:
                print(f"Error: {response.status_code}, {response.text}")
                time.sleep(5)
        except requests.exceptions.Timeout:
            print("Request timed out. Retrying...")
            time.sleep(5)
        except Exception as e:
            print(f"Exception occurred: {e}")
            time.sleep(5)
        attempt += 1
    return None

# ฟังก์ชันสำหรับบันทึก response ที่สำเร็จ
def log_successful_response(response, log_file):
    with open(log_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([response.request.url, response.status_code, response.json()])

# ฟังก์ชันสำหรับบันทึกรายการที่ข้าม
def log_skipped_request(item, log_file):
    with open(log_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([item["POLE_NAME"], item["LON"], item["LAT"]])

# ฟังก์ชันสำหรับสร้าง Location
def createLocation(cctvDetail, headers, log_file):
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
    response = retry_request(requests.post, (url,), {'headers': headers, 'data': payload})
    if response is not None:
        res_json = response.json()
        cctvDetail["LOCATION_ID"] = res_json["@iot.id"]
        log_successful_response(response, log_file)
    else:
        log_skipped_request(cctvDetail, log_file)
    time.sleep(2)
    return cctvDetail

# ฟังก์ชันสำหรับสร้าง Thing
def createThing(cctvDetail, location_id , headers, log_file):
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
    response = retry_request(requests.post, (url,), {'headers': headers, 'data': payload})
    if response is not None:
        res_json = response.json()
        cctvDetail["THING_ID"] = res_json["@iot.id"]
        log_successful_response(response, log_file)
    else:
        log_skipped_request(cctvDetail, log_file)
    time.sleep(2)
    return cctvDetail

# ฟังก์ชันสำหรับสร้าง FeatureOfInterest
def createFeatureOfInterest(cctvDetail , headers, log_file):
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
    response = retry_request(requests.post, (url,), {'headers': headers, 'data': payload})
    if response is not None:
        res_json = response.json()
        cctvDetail["FEATUREOFINTEREST_ID"] = res_json["@iot.id"]
        log_successful_response(response, log_file)
    else:
        log_skipped_request(cctvDetail, log_file)
    time.sleep(2)
    return cctvDetail

# ฟังก์ชันสำหรับเพิ่มข้อมูล POLE
def Insert_pole():
    success_log_file = os.path.join(output_dir, 'successful_responses.csv')
    skipped_log_file = os.path.join(output_dir, 'skipped_requests.csv')
    for path in os.listdir(dir_path):  # path ของไฟล์ CSV
        if os.path.isfile(os.path.join(dir_path, path)):
            print('test', os.path.join(dir_path, path))  # ตรวจสอบ path

            out_dict = []  # CSV
            with open(os.path.join(dir_path, path), encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                count = 0
                prev_name = ''
                locationid = ''
                thingid = ''
                featureid = ''
                i = 1
                for row in csv_reader:
                    print("----- i =", i)

                    if row['POLE_NAME'] != prev_name:
                        prev_name = row['POLE_NAME']

                        # ตรวจสอบว่าชื่อ POLE_NAME มีอยู่ใน things data หรือไม่
                        if row['POLE_NAME'] in things_df['name'].values:
                            # บันทึกข้อมูลที่ซ้ำกันลงในไฟล์ CSV
                            match_file_path = os.path.join(check_before_up_dir, 'poleซ้ำกล้องไม่แอด.csv')
                            with open(match_file_path, mode='a', newline='', encoding='utf-8') as file:
                                writer = csv.writer(file)
                                if os.path.getsize(match_file_path) == 0:
                                    writer.writerow(['POLE_NAME', 'LON', 'LAT'])  # เขียน header ถ้าไฟล์ว่าง
                                writer.writerow([row['POLE_NAME'], row['LON'], row['LAT']])
                            print(f"Duplicate found: {row['POLE_NAME']} not added.")
                            continue

                        # สร้าง location
                        out = createLocation(row, headers, success_log_file)
                        if "LOCATION_ID" not in out:
                            continue  # ข้ามรายการถ้าไม่ได้รับ LOCATION_ID

                        locationid = out['LOCATION_ID']

                        # สร้าง thing
                        out = createThing(out, locationid, headers, success_log_file)
                        if "THING_ID" not in out:
                            continue  # ข้ามรายการถ้าไม่ได้รับ THING_ID

                        thingid = out["THING_ID"]

                        # สร้าง feature of interest
                        out = createFeatureOfInterest(out, headers, success_log_file)
                        if "FEATUREOFINTEREST_ID" not in out:
                            continue  # ข้ามรายการถ้าไม่ได้รับ FEATUREOFINTEREST_ID

                        featureid = out["FEATUREOFINTEREST_ID"]

                        out_dict.append(out)
                        count += 1
                    else:
                        out_dict.append(row)
                        out_dict[i-1]["LOCATION_ID"] = locationid
                        out_dict[i-1]["THING_ID"] = thingid
                        out_dict[i-1]["FEATUREOFINTEREST_ID"] = featureid

                    i += 1
                    time.sleep(2)  # เพิ่มดีเลย์เป็น 2 วินาทีเพื่อลดโหลดเซิร์ฟเวอร์

                print("-------- thing count = %d" % count)  # แสดงจำนวน things

            field_names = list(out_dict[0].keys())
            split_txt = os.path.join(dir_path, path).split('\\')
            name_text = split_txt[-1].split('.')
            file_save = f'C:\\Users\\Demose\\Desktop\\luilayout\\val\\Playground_UploadData-main-main\\Playground_UploadData-main-main\\CSV - larry1\\CCTV-out\\{name_text[0]}-out.csv'
            completeName = os.path.join(file_save)
            with open(completeName, 'w', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=field_names)
                writer.writeheader()
                writer.writerows(out_dict)

# สร้าง Thread สำหรับฟังก์ชัน Insert_pole
thread1 = threading.Thread(target=Insert_pole)

# เริ่มการทำงานของ Thread
thread1.start()

# รอให้ Thread ทำงานเสร็จ
thread1.join()

print("ทำงานเสร็จสิ้น")

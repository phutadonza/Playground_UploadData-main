import csv
import requests
import json
import os
import threading
from host.server import SERVER
from host.api import API

def ค้นหาsensorId(รายละเอียด, headers):
    url = f"{SERVER}/core/api/streaming/v1.1/Sensors?$filter=name eq '{รายละเอียด['CAMERA_NAME']}'"
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        results = response.json()
        if results["value"]:
            return results["value"][0]["@iot.id"]
    print(f"ไม่พบเซ็นเซอร์สำหรับ {รายละเอียด['CAMERA_NAME']}")
    return None

def ลบเซ็นเซอร์(sensor_id, headers):
    url = f"{SERVER}/core/api/streaming/v1.1/Sensors({sensor_id})"
    
    while True:
        response = requests.request("DELETE", url, headers=headers)
        if response.status_code == 200 or response.status_code == 204:
            print(f"ลบเซ็นเซอร์ {sensor_id} เรียบร้อยแล้ว")
            break
        else:
            print(f"เกิดข้อผิดพลาดขณะลบเซ็นเซอร์ {sensor_id}: {response.text}")
            continue

def ลบเซ็นเซอร์จากCSV(file_path, headers):
    if os.path.isfile(file_path):
        with open(file_path, encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                sensor_id = ค้นหาsensorId(row, headers)
                if sensor_id:
                    print(f"เซ็นเซอร์ที่จะลบ: {row['CAMERA_NAME']} (ID: {sensor_id})")
                    confirm = input("พิมพ์ 'del' เพื่อยืนยันการลบ: ")
                    if confirm.lower() == 'del':
                        ลบเซ็นเซอร์(sensor_id, headers)
                    else:
                        print("ยกเลิกการลบเซ็นเซอร์นี้")

# เส้นทางไปยังไฟล์ CSV ที่มีรายชื่อเซ็นเซอร์ที่ต้องการลบ
csv_file_path = r'C:\Users\phutadon\OneDrive\Desktop\Playground_UploadData-main\CSV - larry1\CCTV-out\ชื่อไฟล์ของคุณ.csv'

headers = {
    'API-Key': API,
    'Content-Type': 'application/json'
}

def งานลบเซ็นเซอร์():
    ลบเซ็นเซอร์จากCSV(csv_file_path, headers)

# สร้างเธรดสำหรับงานลบเซ็นเซอร์
thread = threading.Thread(target=งานลบเซ็นเซอร์)

# เริ่มเธรด
thread.start()

# รอให้เธรดทำงานเสร็จ
thread.join()

print("ลบเซ็นเซอร์ทั้งหมดเรียบร้อยแล้ว")

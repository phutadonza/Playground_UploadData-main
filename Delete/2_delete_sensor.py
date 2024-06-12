import csv
import requests
import json
import os
import threading
SERVER = 'http://cctv.naimueang.com:30800'
API = 'a4pddFpUwhZ0We6ILSQcFWd1w0LiUoHqc8kFXKgrZY615fjLXJpvHpaZXldIj0QW'

def ค้นหาsensorId(รายละเอียด, headers):
    url = f"{SERVER}/core/api/streaming/v1.1/Sensors?name={รายละเอียด['CAMERA_NAME']}*"
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        results = response.json()
        if results["value"]:
            return results["value"]
    else:
        print(f"เกิดข้อผิดพลาดขณะค้นหาเซ็นเซอร์: {response.status_code} {response.text}")
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
            print(f"เกิดข้อผิดพลาดขณะลบเซ็นเซอร์ {sensor_id}: {response.status_code} {response.text}")
            break

def แสดงเซ็นเซอร์ที่จะลบ(sensors_to_delete):
    print("\nรายการเซ็นเซอร์ที่จะลบ:")
    for row in sensors_to_delete:
        for sensor in row['sensors']:
            print(f"เซ็นเซอร์: {row['CAMERA_NAME']} (ID: {sensor['@iot.id']})")
    confirm = input("พิมพ์ 'del' เพื่อยืนยันการลบเซ็นเซอร์ทั้งหมด: ")
    return confirm.lower() == 'del'

def ลบเซ็นเซอร์จากCSV(file_path, headers):
    sensors_to_delete = []
    
    if os.path.isfile(file_path):
        with open(file_path, encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                sensors = ค้นหาsensorId(row, headers)
                if sensors:
                    sensors_to_delete.append({
                        'CAMERA_NAME': row['CAMERA_NAME'],
                        'sensors': sensors
                    })
    
    if sensors_to_delete:
        if แสดงเซ็นเซอร์ที่จะลบ(sensors_to_delete):
            for row in sensors_to_delete:
                for sensor in row['sensors']:
                    ลบเซ็นเซอร์(sensor['@iot.id'], headers)
        else:
            print("ยกเลิกการลบเซ็นเซอร์ทั้งหมด")

# เส้นทางไปยังไฟล์ CSV ที่มีรายชื่อเซ็นเซอร์ที่ต้องการลบ
csv_file_path = r'C:\Users\phutadon\OneDrive\Desktop\Playground_UploadData-main\CSV - larry1\CCTV-out\NT_Camera_29_01_24_for_me_-_500-out.csv'

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

print("กระบวนการเสร็จสิ้น")

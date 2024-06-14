import csv
import requests
import os
import json

SERVER = 'https://bkk.larry-cctv.com'
API = 'k3hqivYfUBAEE7BoL1745jQE4PGS0Vq8CL755gMen1tm1shTatHSkyilgi1YnGGa'

def ค้นหาsensorId(รายละเอียด, headers):
    url = f"{SERVER}/core/api/streaming/v1.1/Sensors?name={รายละเอียด['CAMERA_NAME']}*"
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        results = response.json()
        # print(f"ผลลัพธ์จาก API: {json.dumps(results, indent=2, ensure_ascii=False)}")  # พิมพ์ผลลัพธ์ JSON ที่ได้รับทั้งหมด
        if "value" in results and results["value"] and results["@iot.count"] > 0:
            print(results["value"])
            return results["value"]
        else:
            print(f"ไม่พบเซ็นเซอร์สำหรับ {รายละเอียด['CAMERA_NAME']}")
            return None
    elif response.status_code == 404:
        print(f"ไม่พบเซ็นเซอร์สำหรับ {รายละเอียด['CAMERA_NAME']}: {response.status_code} Not Found")
    elif response.status_code == 401:
        print(f"การเข้าถึงถูกปฏิเสธ (Unauthorized): {response.status_code} {response.text}")
    elif response.status_code == 403:
        print(f"การเข้าถึงถูกปฏิเสธ (Forbidden): {response.status_code} {response.text}")
    else:
        print(f"เกิดข้อผิดพลาดขณะค้นหาเซ็นเซอร์: {response.status_code} {response.text}")
    return None

def แสดงเซ็นเซอร์(sensors):
    print("\nรายการเซ็นเซอร์ที่พบ:")
    for row in sensors:
        for sensor in row['sensors']:
            print(f"เซ็นเซอร์: {row['CAMERA_NAME']} (ID: {sensor['@iot.id']})")
            print(json.dumps(sensor, indent=2, ensure_ascii=False))  # แสดงรายละเอียดของเซ็นเซอร์ที่พบ

def ลบเซ็นเซอร์(sensor_id, headers):
    url = f"{SERVER}/core/api/streaming/v1.1/Sensors({sensor_id})"
    response = requests.request("DELETE", url, headers=headers)
    if response.status_code == 200 or response.status_code == 204:
        print(f"ลบเซ็นเซอร์ {sensor_id} เรียบร้อยแล้ว")
    else:
        print(f"เกิดข้อผิดพลาดขณะลบเซ็นเซอร์ {sensor_id}: {response.status_code} {response.text}")

def ค้นหาเซ็นเซอร์จากCSV(file_path, headers):
    sensors_found = []
    
    if os.path.isfile(file_path):
        with open(file_path, encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                sensors = ค้นหาsensorId(row, headers)
                if sensors:
                    sensors_found.append({
                        'CAMERA_NAME': row['CAMERA_NAME'],
                        'sensors': sensors
                    })
    
    if sensors_found:
        แสดงเซ็นเซอร์(sensors_found)
        confirm = input("พิมพ์ 'del' เพื่อยืนยันการลบเซ็นเซอร์ทั้งหมด: ")
        if confirm.lower() == 'del':
            for row in sensors_found:
                for sensor in row['sensors']:
                    ลบเซ็นเซอร์(sensor['@iot.id'], headers)
        else:
            print("ยกเลิกการลบเซ็นเซอร์ทั้งหมด")
    else:
        print("ไม่พบเซ็นเซอร์ใดๆในไฟล์ CSV")

# เส้นทางไปยังไฟล์ CSV ที่มีรายชื่อเซ็นเซอร์ที่ต้องการค้นหา
csv_file_path = r'C:\Users\phutadon\OneDrive\Desktop\Playground_UploadData-main\CSV - larry1\link\แก้.csv'

headers = {
    'API-Key': API,
    'Content-Type': 'application/json'
}

# เรียกใช้ฟังก์ชันค้นหาเซ็นเซอร์จากไฟล์ CSV
ค้นหาเซ็นเซอร์จากCSV(csv_file_path, headers)

import requests
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

# ตั้งค่า headers สำหรับ API
headers = {
    'API-Key': API_test,
    'Content-Type': 'application/json'
}

def get_sensor_by_name(sensor_name, headers):
    url = f"{SERVER_test}/core/api/streaming/v1.1/Sensors"
    params = {
        'name': sensor_name
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        sensors = response.json()
        if sensors['value']:
            return sensors['value'][0]
        else:
            print(f"Sensor '{sensor_name}' not found.")
            return None
    else:
        print(f"Error fetching sensor: {response.text}")
        return None

def delete_sensor(sensor_id, headers):
    url = f"{SERVER_test}/core/api/streaming/v1.1/Sensors({sensor_id})?forever=true"
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print(f"Sensor with ID {sensor_id} successfully deleted.")
    else:
        print(f"Error deleting sensor: {response.text}")

def delete_sensor_by_name(sensor_name):
    sensor = get_sensor_by_name(sensor_name, headers)
    if sensor:
        print(f"Sensor found: {sensor}")
        confirm = input("Type 'del' to confirm deletion: ")
        if confirm.lower() == 'del':
            delete_sensor(sensor['@iot.id'], headers)
        else:
            print("Deletion canceled.")
    else:
        print(f"Sensor '{sensor_name}' not found.")

# ตัวอย่างการลบเซ็นเซอร์โดยใช้ชื่อเซ็นเซอร์
sensor_name_to_delete = "ชื่อเซ็นเซอร์ที่ต้องการลบ"
delete_sensor_by_name(sensor_name_to_delete)

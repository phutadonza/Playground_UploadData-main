import requests
import pandas as pd
import json
import os
from host.server import SERVER
from host.api import API

# กำหนดพาธของไดเรกทอรีที่ไฟล์ CSV อยู่
dir_path = r'C:\Users\phutadon\OneDrive\Desktop\Playground_UploadData-main\CSV - larry1\CCTV-out-dt'


# ดึงรายชื่อไฟล์ในไดเรกทอรี
files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]

# เลือกไฟล์แรกเพื่อการทดสอบ
test_file = files[0]
print(f"Testing with file: {test_file}")

# อ่านไฟล์ CSV เข้า DataFrame
data = pd.read_csv(os.path.join(dir_path, test_file))

# กำหนด API endpoint
url = f"{SERVER}/core/api/streaming/v1.1/Observations"

# ตั้งค่า headers
headers = {
    'Content-Type': 'application/json',
    'API-Key': API
}

# เลือกแถวแรกเพื่อการทดสอบ
i = 0
datastream = data._get_value(i, 'DATASTREAM_ID (Live)')
name = data._get_value(i, 'CAMERA_NAME')
link = f"https://rtc-bkk-bma-ba-2-165.larry-cctv.com/api/stream.mp4?src={name}&mp4=flac"

# แสดงค่า datastream ID และชื่อกล้อง
print(f"Datastream ID: {datastream}, Camera Name: {name}")
print(f"Generated link: {link}")

# สร้าง payload
payload = json.dumps({
    "result": link,
    "resultType": "string",
    "Datastream": {"@iot.id": datastream}
})

# แสดง payload
print(f"Payload: {payload}")

# ส่งคำขอ POST และแสดงผลลัพธ์
response = requests.post(url, headers=headers, data=payload)

# แสดงรหัสสถานะและข้อความตอบกลับ
print(f"Response Status Code: {response.status_code}")
print(f"Response Text: {response.text}")

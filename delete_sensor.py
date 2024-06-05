import requests
from host.api import API
from host.server import SERVER
# http://cctv.naimueang.com:30800/core/api/streaming/v1.1/Datastreams  ## ข้อมูลที่อยู่ใน sensor อีกที
# /streaming/v1.1/Sensors(64673cc5b3045bdd556d0c9d)?forever=true
# http://cctv.naimueang.com:30800/core/api/streaming/v1.1/Sensors?$top=150&$orderby=id%20desc


headers = {
    'API-Key': API,
    'Content-Type': 'application/json'
    }

# URL เพื่อดึงข้อมูล Location ทั้งหมด
sensor_url = f"{SERVER}/core/api/streaming/v1.1/Sensors?$top=10000&$orderby=id%20desc"

# ส่งคำขอ GET เพื่อดึงข้อมูล Location ทั้งหมด
response = requests.get(sensor_url, headers=headers)

# ตรวจสอบว่าคำขอ GET สำเร็จหรือไม่
if response.status_code == 200:
    # แปลงการตอบสนอง JSON
    # print(response.json()) ## test debug

    sensor_data = response.json()
    
    # ตรวจสอบว่ามีคีย์ 'value' ในข้อมูลการตอบสนองหรือไม่
    if 'value' in sensor_data:
        # วนลูปผ่าน Location แต่ละรายการและดึงค่า @iot.id
        for sensor in sensor_data['value']:
            sensor_id = sensor.get('@iot.id')
            # print(sensor_id) ## test debug 
            
            if sensor_id:
                # สร้าง URL สำหรับคำขอ DELETE
                delete_url = f"{SERVER}/core/api/streaming/v1.1/Sensors({sensor_id})?forever=true"
                
                # ส่งคำขอ DELETE
                delete_response = requests.delete(delete_url, headers=headers)
                # print(delete_response.json()) ## test debug with get

                # แสดงผลลัพธ์ของคำขอ DELETE
                if delete_response.status_code == 204:
                    print(f"ลบ Sensor ที่มี ID: {sensor_id} สำเร็จ")
                else:
                    print(f"ลบ Sensor ที่มี ID: {sensor_id} ไม่สำเร็จ รหัสสถานะ: {delete_response.status_code}")
    else:
        print("ไม่พบ Sensor ในการตอบสนอง")
else:
    print(f"การดึงข้อมูล Sensor ไม่สำเร็จ รหัสสถานะ: {response.status_code}")
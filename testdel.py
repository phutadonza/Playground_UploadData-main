import requests
from host.server import SERVER
from host.api import API
# กำหนด URL ของเซิร์ฟเวอร์และคีย์ API

# ตั้งค่า headers สำหรับการส่งคำขอ
headers = {
    'API-Key': API,
    'Content-Type': 'application/json'
}

# URL เพื่อดึงข้อมูล Location ทั้งหมด
locations_url = f"{SERVER}/core/api/streaming/v1.1/Locations?$top=10000&$orderby=id%20desc"

# ส่งคำขอ GET เพื่อดึงข้อมูล Location ทั้งหมด
response = requests.get(locations_url, headers=headers)

# ตรวจสอบว่าคำขอ GET สำเร็จหรือไม่
if response.status_code == 200:
    # แปลงการตอบสนอง JSON
    locations_data = response.json()
    
    # ตรวจสอบว่ามีคีย์ 'value' ในข้อมูลการตอบสนองหรือไม่
    if 'value' in locations_data and len(locations_data['value']) > 0:
        # ดึงค่า @iot.id ของ Location ตัวแรก
        location_id = locations_data['value'][0].get('@iot.id')
        
        if location_id:
            # สร้าง URL สำหรับคำขอ DELETE
            delete_url = f"{SERVER}/core/api/streaming/v1.1/Locations({location_id})"
            
            # ส่งคำขอ DELETE
            delete_response = requests.delete(delete_url, headers=headers)
            
            # แสดงผลลัพธ์ของคำขอ DELETE
            if delete_response.status_code == 204:
                print(f"ลบ Location ที่มี ID: {location_id} สำเร็จ")
            else:
                print(f"ลบ Location ที่มี ID: {location_id} ไม่สำเร็จ รหัสสถานะ: {delete_response.status_code}")
        else:
            print("ไม่พบ @iot.id ใน Location ตัวแรก")
    else:
        print("ไม่พบ Location ในการตอบสนอง")
else:
    print(f"การดึงข้อมูล Location ไม่สำเร็จ รหัสสถานะ: {response.status_code}")

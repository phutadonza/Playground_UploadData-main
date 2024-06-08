import requests
from host.server import SERVER
from host.api import API


# METHOD "delete"

# http://cctv.naimueang.com:30800/core/api/streaming/v1.1/Locations  ## ข้อมูลหัวข้อ Location
# {SERVER}/core/api/streaming/v1.1/Locations(645dd5e11c2b2dc6eb684348)
# http://cctv.naimueang.com:30800/core/api/streaming/v1.1/Locations?$top=10000&$orderby=id%20desc  ## all Location in web show


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
    if 'value' in locations_data:
        # วนลูปผ่าน Location แต่ละรายการและดึงค่า @iot.id
        for location in locations_data['value']:
            location_id = location.get('@iot.id')
            
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
        print("ไม่พบ Location ในการตอบสนอง")
else:
    print(f"การดึงข้อมูล Location ไม่สำเร็จ รหัสสถานะ: {response.status_code}")
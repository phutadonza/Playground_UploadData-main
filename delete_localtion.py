import requests
from host.server import SERVER
from host.api import API


# METHOD "delete"

# http://cctv.naimueang.com:30800/core/api/streaming/v1.1/Locations  ## ข้อมูลหัวข้อ Location
# {SERVER}/core/api/streaming/v1.1/Locations(645dd5e11c2b2dc6eb684348)


headers = {
    'API-Key': API,
    'Content-Type': 'application/json'
    }

# URL ของ API สำหรับดึงข้อมูล Locations ทั้งหมด
locations_url = f"{SERVER}/core/api/streaming/v1.1/Locations"

# ส่งคำขอ GET เพื่อดึงข้อมูลทั้งหมด
response = requests.get(locations_url, headers=headers)

print(response.json())

# ตรวจสอบสถานะการตอบกลับ
# if response.status_code == 200:
locations = response.json()
    
#     # ตรวจสอบว่ามีข้อมูลหรือไม่
if 'value' in locations:
    for location in locations['value']:
        if "@iot.id" in location:
            print(location['@iot.id'])
#                 iot_id = location["@iot.id"]
                
#                 # URL สำหรับลบ location ตาม @iot.id
#                 delete_url = f"{SERVER}/core/api/streaming/v1.1/Locations({iot_id})"
                
#                 # ส่งคำขอ DELETE เพื่อทำการลบ
#                 delete_response = requests.delete(delete_url, headers=headers)
                
#                 # ตรวจสอบสถานะการตอบกลับของการลบ
#                 if delete_response.status_code == 200:
#                     print(f"Resource with @iot.id {iot_id} deleted successfully.")
#                 else:
#                     print(f"Error {delete_response.status_code}: could not delete resource with @iot.id {iot_id}.")
#     else:
#         print("No locations found.")
# else:
#     print(f"Error {response.status_code}: could not retrieve locations.")
    
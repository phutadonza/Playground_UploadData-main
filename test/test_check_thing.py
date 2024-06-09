import requests
from host.api import API
from host.server import SERVER

headers = {
            'API-Key':API,
            'Content-Type': 'application/json'      
        }
# URL ของ API
url = f"{SERVER}/core/api/streaming/v1.1/Things?$top=10000&$orderby=id%20desc"
# ส่งคำขอ GET ไปที่ API
response = requests.get(url,headers=headers)
# print(response.json())
# ตรวจสอบสถานะการตอบสนอง
if response.status_code == 200:
    data = response.json()
    
    # ดึงข้อมูล value จาก JSON
    items = data['value']
    
    # ตรวจสอบชื่อที่ซ้ำกัน
    names = [item['name'] for item in items]
    duplicate_names = set([name for name in names if names.count(name) > 1])
    
    if duplicate_names:
        print(f"Duplicate names found: {duplicate_names}")
    else:
        print("No duplicate names found.")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")

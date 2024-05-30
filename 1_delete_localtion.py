import requests
from host.server import SERVER
from host.api import API

# http://cctv.naimueang.com:30800/core/api/streaming/v1.1/Things(6656a8e4e653d124cbed72ad)?forever=true

# METHOD "delete"

# http://cctv.naimueang.com:30800/core/api/streaming/v1.1/Datastreams  ## ข้อมูลที่อยู่ใน sensor อีกที

headers = {
    'API-Key': API,
    'Content-Type': 'application/json'
    }

url = f"{SERVER}/core/api/streaming/v1.1/Datastreams"

response = requests.get(url,headers=headers)
if response.status_code == 200 :
    print(response.json())

else :
    print("Error 404 can not found")
    
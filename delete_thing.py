import requests
from host.api import API
from host.server import SERVER
# http://cctv.naimueang.com:30800/core/api/streaming/v1.1/Things(64702b2f5198e573b4dbf117)  ## ข้อมูลหัวข้อ Solution(Thing)
# http://cctv.naimueang.com:30800/core/api/streaming/v1.1/Things?$top=150&$orderby=id%20desc

headers = {
    'API-Key': API,
    'Content-Type': 'application/json'
    }

thing_url = f'{SERVER}/core/api/streaming/v1.1/Things?$top=10000&$orderby=id%20desc' 
response = requests.get(thing_url,headers=headers)

if response.status_code == 200:

    thing_data = response.json()


    if 'value' in thing_data:

        for thing in thing_data['value']:
            thing_id = thing.get('@iot.id')
            # print(thing_id)  ## test debug
            if thing_id:
                delete_url = f"{SERVER}/core/api/streaming/v1.1/Things({thing_id})"

                delete_response = requests.delete(delete_url, headers = headers)

                # print(delete_response.json()) ## test debug
                if delete_response.status_code == 204:
                    print(f"ลบ Thing ที่มี ID: {thing_id} สำเร็จ")
                else:
                    print(f"ลบ Thing ที่มี ID: {thing_id} ไม่สำเร็จ รหัสสถานะ: {delete_response.status_code}")
    else:
        print("ไม่พบ Thing ในการตอบสนอง")
else:
    print(f"การดึงข้อมูล Thing ไม่สำเร็จ รหัสสถานะ: {response.status_code}")
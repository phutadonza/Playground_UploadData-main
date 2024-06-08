import requests
from host.server import SERVER
from host.api import API

def delete_latest_location():
    # ตั้งค่า headers สำหรับการส่งคำขอ
    headers = {
        'API-Key': API,
        'Content-Type': 'application/json'
    }

    # URL เพื่อดึงข้อมูล Location ทั้งหมด
    locations_url = f"{SERVER}/core/api/streaming/v1.1/Locations?$top=10000&$orderby=id%20desc"

    try:
        # ส่งคำขอ GET เพื่อดึงข้อมูล Location ทั้งหมด
        response = requests.get(locations_url, headers=headers)

        # ตรวจสอบว่าคำขอ GET สำเร็จหรือไม่
        response.raise_for_status()

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
    except requests.exceptions.RequestException as e:
        print(f"เกิดข้อผิดพลาด: {e}")


def delete_first_thing():
    # ตั้งค่า headers สำหรับการส่งคำขอ
    headers = {
        'API-Key': API,
        'Content-Type': 'application/json'
    }

    # URL เพื่อดึงข้อมูล Thing ทั้งหมด
    thing_url = f'{SERVER}/core/api/streaming/v1.1/Things?$top=150&$orderby=id%20desc'

    try:
        # ส่งคำขอ GET เพื่อดึงข้อมูล Thing ทั้งหมด
        response = requests.get(thing_url, headers=headers)

        # ตรวจสอบว่าคำขอ GET สำเร็จหรือไม่
        response.raise_for_status()

        # แปลงการตอบสนอง JSON
        thing_data = response.json()

        # ตรวจสอบว่ามีคีย์ 'value' ในข้อมูลการตอบสนองหรือไม่
        if 'value' in thing_data and len(thing_data['value']) > 0:
            # ดึงค่า @iot.id ของ Thing ตัวแรก
            thing_id = thing_data['value'][0].get('@iot.id')

            if thing_id:
                # สร้าง URL สำหรับคำขอ DELETE
                delete_url = f"{SERVER}/core/api/streaming/v1.1/Things({thing_id})"

                # ส่งคำขอ DELETE
                delete_response = requests.delete(delete_url, headers=headers)

                # แสดงผลลัพธ์ของคำขอ DELETE
                if delete_response.status_code == 204:
                    print(f"ลบ Thing ที่มี ID: {thing_id} สำเร็จ")
                else:
                    print(f"ลบ Thing ที่มี ID: {thing_id} ไม่สำเร็จ รหัสสถานะ: {delete_response.status_code}")
            else:
                print("ไม่พบ @iot.id ใน Thing ตัวแรก")
        else:
            print("ไม่พบ Thing ในการตอบสนอง")
    except requests.exceptions.RequestException as e:
        print(f"เกิดข้อผิดพลาดในการดึงหรือส่งข้อมูล: {e}")

def delete_first_sensor():
    headers = {
        'API-Key': API,
        'Content-Type': 'application/json'
    }

    # URL เพื่อดึงข้อมูล Sensor ทั้งหมด
    sensor_url = f"{SERVER}/core/api/streaming/v1.1/Sensors?$top=1&$orderby=id%20desc"

    # ส่งคำขอ GET เพื่อดึงข้อมูล Sensor
    response = requests.get(sensor_url, headers=headers)

    # ตรวจสอบว่าคำขอ GET สำเร็จหรือไม่
    if response.status_code == 200:
        # แปลงการตอบสนอง JSON
        sensor_data = response.json()
        
        # ตรวจสอบว่ามีคีย์ 'value' ในข้อมูลการตอบสนองหรือไม่
        if 'value' in sensor_data and len(sensor_data['value']) > 0:
            # ดึงค่า @iot.id ของ Sensor ตัวแรก
            sensor_id = sensor_data['value'][0].get('@iot.id')
            
            if sensor_id:
                # สร้าง URL สำหรับคำขอ DELETE
                delete_url = f"{SERVER}/core/api/streaming/v1.1/Sensors({sensor_id})?forever=true"
                
                # ส่งคำขอ DELETE
                delete_response = requests.delete(delete_url, headers=headers)

                # แสดงผลลัพธ์ของคำขอ DELETE
                if delete_response.status_code == 204:
                    print(f"ลบ Sensor ที่มี ID: {sensor_id} สำเร็จ")
                else:
                    print(f"ลบ Sensor ที่มี ID: {sensor_id} ไม่สำเร็จ รหัสสถานะ: {delete_response.status_code}")
            else:
                print("ไม่พบ ID ของ Sensor")
        else:
            print("ไม่พบ Sensor ในการตอบสนอง")
    else:
        print(f"การดึงข้อมูล Sensor ไม่สำเร็จ รหัสสถานะ: {response.status_code}")

# เรียกใช้ฟังก์ชัน
delete_first_sensor()


# เรียกใช้ฟังก์ชัน
# delete_first_thing()


# เรียกใช้ฟังก์ชัน
# delete_latest_location()

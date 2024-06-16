import pandas as pd
import requests

# อ่านข้อมูลจากไฟล์ CSV
csv_file_path = r'C:\Users\phuta\Desktop\Playground_UploadData-main\CSV - larry1\link\สำเนาของ NT_Camera ไม่ได้อัพ_จะอัพ - จะอัพ_4-out-dt.csv'  # เปลี่ยนเป็นเส้นทางที่ถูกต้องไปยังไฟล์ CSV ของคุณ
data = pd.read_csv(csv_file_path)

# ดึง sensor IDs
sensor_ids = data['SENSOR_ID'].dropna().unique()

# รายละเอียด endpoint ของ API
api_url = 'https://bkk.larry-cctv.com/core/api/streaming/v1.1/'  # URL ของ API ที่ถูกต้อง
headers = {
    'API-Key': 'k3hqivYfUBAEE7BoL1745jQE4PGS0Vq8CL755gMen1tm1shTatHSkyilgi1YnGGa',  # API Key ที่ถูกต้อง
    'Content-Type': 'application/json'
}
delete_endpoint = 'Sensors({sensor_id})?forever=true'

# แสดงข้อมูลทั้งหมดก่อนการลบ
print("เซ็นเซอร์ทั้งหมดที่จะลบ:")
for sensor_id in sensor_ids:
    url = f"{api_url}{delete_endpoint.format(sensor_id=sensor_id)}"
    print(f"URL ที่จะใช้ลบ: {url}")

# ขอให้ผู้ใช้ยืนยันก่อนที่จะลบ sensor ทั้งหมด
confirm = input(f"คุณต้องการลบเซ็นเซอร์ทั้งหมดหรือไม่? (พิมพ์ 'yes' เพื่อลบ): ")

if confirm.lower() == 'yes':
    for sensor_id in sensor_ids:
        url = f"{api_url}{delete_endpoint.format(sensor_id=sensor_id)}"
        response = requests.delete(url, headers=headers)
        
        # พิมพ์รหัสสถานะ HTTP
        print(f"HTTP Status Code: {response.status_code}")
        
        if response.status_code == 204:
            print(f"ลบ sensor ที่มี ID: {sensor_id} สำเร็จ")
        else:
            print(f"ลบ sensor ที่มี ID: {sensor_id} ไม่สำเร็จ รหัสสถานะ: {response.status_code}, ข้อความ: {response.text}")
else:
    print("ยกเลิกการลบเซ็นเซอร์ทั้งหมด")


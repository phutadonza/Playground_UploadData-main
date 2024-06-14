import csv
import requests
import time

# ที่อยู่ของไฟล์ CSV ของคุณ
csv_file_path = r'C:\Users\phutadon\OneDrive\Desktop\Playground_UploadData-main\CSV - larry1\CCTV-out\สำเนาของ NT_Camera ไม่ได้อัพ_จะอัพ - ตัวเหลือง (1)-out.csv'

# รายละเอียดของ API
api_url = 'https://bkk.larry-cctv.com/core/api/streaming/v1.1'  # เปลี่ยนเป็น API endpoint ของคุณ
headers = {
    'API-Key': 'k3hqivYfUBAEE7BoL1745jQE4PGS0Vq8CL755gMen1tm1shTatHSkyilgi1YnGGa',  # เปลี่ยนเป็น token ของคุณถ้าจำเป็น
    'Content-Type': 'application/json'
}

# อ่านไฟล์ CSV
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    rows = list(reader)

# พิมพ์รายการตรวจสอบ
print("\nรายการตรวจสอบ:")
for row in rows:
    print(f"POLE_NAME: {row['POLE_NAME']}, LOCATION_ID: {row['LOCATION_ID']}, THING_ID: {row['THING_ID']}")

# ขอการยืนยันจากผู้ใช้เพื่อลบ
user_input = input("\nคุณต้องการลบทุก Thing และ Location ที่ระบุไว้หรือไม่? พิมพ์ 'ลบ' เพื่อยืนยัน: ")
if user_input.lower() == 'ลบ':
    for row in rows:
        if row['THING_ID'] not in ['Not Found', 'Error']:
            delete_response = requests.delete(f'{api_url}/Things({row["THING_ID"]})', headers=headers)
            if delete_response.status_code in [200, 204]:
                print(f"Thing ที่มี ID {row['THING_ID']} ของเสา {row['POLE_NAME']} ถูกลบเรียบร้อยแล้ว.")
            elif delete_response.status_code == 404:
                print(f"Thing ที่มี ID {row['THING_ID']} ของเสา {row['POLE_NAME']} ไม่พบ อาจจะถูกลบไปแล้ว.")
            else:
                print(f"ไม่สามารถลบ Thing ที่มี ID {row['THING_ID']} ของเสา {row['POLE_NAME']} ได้ รหัสสถานะ: {delete_response.status_code}")
                print(delete_response.text)
            time.sleep(1)  # หน่วงเวลา 1 วินาที
        
        if row['LOCATION_ID'] not in ['Not Found', 'Error']:
            delete_response = requests.delete(f'{api_url}/Locations({row["LOCATION_ID"]})', headers=headers)
            if delete_response.status_code in [200, 204]:
                print(f"Location ที่มี ID {row['LOCATION_ID']} ของเสา {row['POLE_NAME']} ถูกลบเรียบร้อยแล้ว.")
            elif delete_response.status_code == 404:
                print(f"Location ที่มี ID {row['LOCATION_ID']} ของเสา {row['POLE_NAME']} ไม่พบ อาจจะถูกลบไปแล้ว.")
            else:
                print(f"ไม่สามารถลบ Location ที่มี ID {row['LOCATION_ID']} ของเสา {row['POLE_NAME']} ได้ รหัสสถานะ: {delete_response.status_code}")
                print(delete_response.text)
            time.sleep(1)  # หน่วงเวลา 1 วินาที
else:
    print("การลบถูกยกเลิก.")

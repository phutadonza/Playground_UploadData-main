import os
import pandas as pd
import requests
import time

SERVER='https://bkk.larry-cctv.com'
API='k3hqivYfUBAEE7BoL1745jQE4PGS0Vq8CL755gMen1tm1shTatHSkyilgi1YnGGa'
headers = {
    'API-Key': API,
    'Content-Type': 'application/json'
}

# ฟังก์ชั่นในการดึงข้อมูลจาก API
def fetch_sensor_data(sensor_name, retries=3, timeout=10):
    url = f"{SERVER}/core/api/streaming/v1.1/Sensors?name={sensor_name}*"
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            if response.status_code == 200:
                data = response.json()
                print(data)
                if data['@iot.count'] > 0:
                    return [sensor['name'] for sensor in data['value']]
            elif response.status_code == 500:
                print(f"Server error (500) for sensor: {sensor_name}")
                break
        except requests.exceptions.Timeout:
            print(f"Request timed out for sensor: {sensor_name}, retrying... ({attempt + 1}/{retries})")
        except requests.exceptions.RequestException as e:
            print(f"Request failed for sensor: {sensor_name} with error: {e}")
            break
        attempt += 1
        time.sleep(1)
    return None

# ไดเรกทอรีที่เก็บไฟล์ CSV
directory = r"C:\Users\phutadon\OneDrive\Desktop\Playground_UploadData-main\CSV - larry1\CCTV-out"

# อ่านไฟล์ CSV ในไดเรกทอรี
csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

# สร้างลิสต์เพื่อเก็บผลลัพธ์
results = []

for file in csv_files:
    file_path = os.path.join(directory, file)
    df = pd.read_csv(file_path)

    # แสดงข้อความเมื่อเริ่มต้นการทำงาน
    print(f"Checking sensors in file: {file}")

    # ตรวจสอบแต่ละชื่อในคอลัมน์ CAMERA_NAME
    for sensor_name in df['CAMERA_NAME']:
        found_sensor_names = fetch_sensor_data(sensor_name)
        if found_sensor_names:
            for found_sensor_name in found_sensor_names:
                results.append((sensor_name, "Found", file, found_sensor_name))
        else:
            results.append((sensor_name, "Not Found", file, None))
        # ทำการดีเลย์ 0.2 วินาที
        time.sleep(0.2)

# แสดงข้อความเมื่อเสร็จสิ้นการทำงาน
print("Finished checking all sensors.")

# แปลงผลลัพธ์เป็น DataFrame
results_df = pd.DataFrame(results, columns=['CAMERA_NAME', 'Status', 'File', 'Found_Sensor_Name'])

# บันทึกผลลัพธ์เป็นไฟล์ CSV ใหม่
results_output_path = os.path.join(directory, "results.csv")
results_df.to_csv(results_output_path, index=False)

# แสดงข้อความเมื่อเสร็จสิ้นการบันทึกผลลัพธ์
print(f"Results saved to '{results_output_path}'.")

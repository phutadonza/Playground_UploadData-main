import os
import pandas as pd
import requests

# ระบุไดเรกทอรีที่เก็บไฟล์ CSV
dir_path = r'C:\Users\phutadon\OneDrive\Desktop\Playground_UploadData-main\CSV - larry1\CCTV'

# สร้างรายการไฟล์ CSV ทั้งหมดในไดเรกทอรี
csv_files = [f for f in os.listdir(dir_path) if f.endswith('.csv')]

# อ่านและรวมข้อมูลจากไฟล์ CSV ทั้งหมด
dataframes = []
for file in csv_files:
    file_path = os.path.join(dir_path, file)
    df = pd.read_csv(file_path)
    dataframes.append(df[['CAMERA_NAME', 'NVR RTSP MAIN']])

# รวมข้อมูลทั้งหมดเป็น DataFrame เดียว
combined_df = pd.concat(dataframes, ignore_index=True)

# URL ของ API
api_url = "https://rtc-mie.i-bitz.world/api/streams"

# ส่งข้อมูลไปยัง API สำหรับแต่ละแถวใน DataFrame
for index, row in combined_df.iterrows():
    name = row['CAMERA_NAME']
    src = row['NVR RTSP MAIN']
    
    # แปลง & เป็น %26
    src_encoded = src.replace("&", "%26")
    src_encoded='ffmpeg:'+src_encoded
    # สร้าง URL สำหรับแต่ละแถว
    url = f"{api_url}?name={name}&src={src_encoded}"
    
    # ส่ง PUT request ไปยัง URL
    response = requests.put(url)
    
    # ตรวจสอบสถานะการตอบสนอง
    if response.status_code == 200:
        print(f"Success for index {name}")
    else:
        print(f"Error for index {index}: {response.status_code}")

# แสดงผล DataFrame รวม
print(combined_df)

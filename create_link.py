import os
import pandas as pd

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

# ระบุไดเรกทอรีที่ต้องการบันทึกไฟล์ใหม่
output_dir = r'C:\Users\phutadon\OneDrive\Desktop\Playground_UploadData-main\CSV - larry1\test'

# ตรวจสอบว่าไดเรกทอรีที่ต้องการบันทึกไฟล์ใหม่มีอยู่แล้วหรือไม่ ถ้าไม่มีให้สร้างใหม่
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# ระบุชื่อไฟล์และเส้นทางสำหรับไฟล์ใหม่
output_file = os.path.join(output_dir, 'combined_data.csv')

# บันทึก DataFrame เป็นไฟล์ CSV
combined_df.to_csv(output_file, index=False)

print(f'ข้อมูลถูกบันทึกที่: {output_file}')

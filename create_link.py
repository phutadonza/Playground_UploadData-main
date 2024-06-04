import os
import pandas as pd

# ระบุไดเรกทอรีที่เก็บไฟล์ CSV
dir_path = r'C:\Users\phutadon\OneDrive\Desktop\Playground_UploadData-main\CSV - larry1\CCTV-out-dt'

save_path = r'C:\Users\phutadon\OneDrive\Desktop\Playground_UploadData-main\CSV - larry1\link'

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

# สร้างคอลัมน์ใหม่สำหรับ src_encoded
combined_df['NVR RTSP MAIN ENCODED'] = combined_df['NVR RTSP MAIN'].apply(lambda x: 'ffmpeg:' + x.replace("&", "%26"))

# บันทึกข้อมูลลงในไฟล์ txt
txt_file_path = os.path.join(save_path, 'encoded_urls.txt')
with open(txt_file_path, 'w') as file:
    for index, row in combined_df.iterrows():
        file.write(f"    {row['CAMERA_NAME']}: {row['NVR RTSP MAIN ENCODED']}\n")


# แสดงผล DataFrame รวม
print(combined_df)
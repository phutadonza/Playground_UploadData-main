import os
import pandas as pd

# ระบุไดเรกทอรีที่เก็บไฟล์ CSV
dir_path = r'C:\Users\phutadon\OneDrive\Desktop\Playground_UploadData-main\CSV - larry1\CCTV-out-dt'

save_path = r'C:\Users\phutadon\OneDrive\Desktop\Playground_UploadData-main\CSV - larry1\link'

# สร้างรายการไฟล์ CSV ทั้งหมดในไดเรกทอรี
csv_files = [f for f in os.listdir(dir_path) if f.endswith('.csv')]

# อ่านและรวมข้อมูลจากไฟล์ CSV ทั้งหมด
for file in csv_files:
    file_path = os.path.join(dir_path, file)
    df = pd.read_csv(file_path)
    df_selected = df[['CAMERA_NAME', 'NVR RTSP MAIN']]
    
    # สร้างคอลัมน์ใหม่สำหรับ src_encoded โดยไม่แปลงสัญลักษณ์ &
    df_selected['NVR RTSP MAIN ENCODED'] = 'ffmpeg:' + df_selected['NVR RTSP MAIN']
    
    # สร้างชื่อไฟล์ที่เซฟตามไฟล์ที่อ่านและต่อท้ายด้วย -link
    txt_file_name = os.path.splitext(file)[0] + '-link.txt'
    txt_file_path = os.path.join(save_path, txt_file_name)
    
    # บันทึกข้อมูลลงในไฟล์ txt
    with open(txt_file_path, 'w') as txt_file:
        for index, row in df_selected.iterrows():
            txt_file.write(f"    {row['CAMERA_NAME']}: {row['NVR RTSP MAIN ENCODED']}\n")

    # แสดงผล DataFrame ที่เลือก
    print(df_selected)

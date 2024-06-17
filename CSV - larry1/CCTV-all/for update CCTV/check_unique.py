import pandas as pd
import os

# ตั้งค่าไดเรกทอรีและชื่อไฟล์
output_dir = r'C:\Users\phutadon\OneDrive\Desktop\Playground_UploadData-main\CSV - larry1\CCTV-all'
things_file = os.path.join(output_dir, 'things_data.csv')
sheet_file = os.path.join(output_dir, 'sheet_data.csv')
unique_pole_names_file = os.path.join(output_dir, 'unique_pole_names.csv')

# อ่านไฟล์ CSV
things_df = pd.read_csv(things_file)
sheet_df = pd.read_csv(sheet_file)

# ตรวจสอบค่า POLE_NAME ที่ไม่มีใน things_data
unique_pole_names_df = sheet_df[~sheet_df['POLE_NAME'].isin(things_df['name'])]

# บันทึกค่า POLE_NAME ที่ไม่ซ้ำกันลงในไฟล์ CSV ใหม่
unique_pole_names_df.to_csv(unique_pole_names_file, index=False)

print(f"Unique POLE_NAME data has been written to {unique_pole_names_file}")

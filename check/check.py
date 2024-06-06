import pandas as pd

# อ่านไฟล์ results.csv
results_file_path = r"C:\Users\phutadon\OneDrive\Desktop\Playground_UploadData-main\CSV - larry1\CCTV-out\results.csv"
results_df = pd.read_csv(results_file_path)

# ค้นหา CAMERA_NAME ที่มีชื่อซ้ำกัน
duplicate_camera_names = results_df[results_df.duplicated(['CAMERA_NAME'], keep=False)]

# แสดงข้อมูลชื่อ CAMERA_NAME ที่มีชื่อซ้ำกัน
print(duplicate_camera_names)

# กำหนด path สำหรับบันทึกไฟล์ใหม่
output_path = r"C:\Users\phutadon\OneDrive\Desktop\Playground_UploadData-main\check\duplicate_camera_names.csv"

# บันทึกข้อมูลชื่อ CAMERA_NAME ที่มีชื่อซ้ำกันลงในไฟล์ CSV ใหม่
duplicate_camera_names.to_csv(output_path, index=False)

# แสดงข้อความเมื่อเสร็จสิ้นการบันทึกผลลัพธ์
print(f"Duplicate CAMERA_NAME saved to '{output_path}'.")

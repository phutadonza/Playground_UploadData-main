import csv
import requests
import json
import threading
from host.server import SERVER
from host.api import API
import os


dir_path = r'C:\\Users\\Dell\\Desktop\\CCTV\\Treading\\CSV - larry1\\CCTV\\'

headers = {
    'API-Key': API,
    'Content-Type': 'application/json'
    }

def Insert_pole():
    for path in os.listdir(dir_path):  #path
        if os.path.isfile(os.path.join(dir_path, path)):
           # print(os.path.join(dir_path, path))
            with open( os.path.join(dir_path, path) , encoding='utf-8') as csv_file:
                print(os.path.join(dir_path, path))
                csv_reader = csv.DictReader(csv_file)
                count = 1
                for row in csv_reader:
                    #print(row['CAMERA_NAME'])
                    get_pole(row['CAMERA_NAME'], count)
                    count =count+1
                    
def get_pole(row,num):

    url = f"https://app.larry-cctv.com/core/api/streaming/v1.1/Sensors?name=*{row}*&$top=150&$orderby=id%20desc"
    

    response = requests.get(url,headers=headers)

    response_json = response.json()
    #print(response_json['@iot.count'])  #////  @iot.count ==  7 
    #print(response_json.status_code)  #////  @iot.count ==  7 
    #if response_json['@iot.count'] <= 0 :
        #print(num,row,'Have Data Not')
    #    print(num)
    if response_json['@iot.count'] > 0 :
        print(num,row ,'Have Data ')
    
    

    #for i in range(len(response_json['value'])) :
        #print(i, " ID_SENSOR :",response_json['value'][i]['@iot.id']," NAME :",response_json['value'][i]['name'])
    #    print(i,response_json['value'][i]['name'])




                    
                    
            
# สร้าง Thread สำหรับแต่ละฟังก์ชัน
thread1 = threading.Thread(target=Insert_pole)

# เริ่มการทำงานของแต่ละ Thread
thread1.start()

# รอให้ทั้งสอง Thread ทำงานเสร็จ
thread1.join()

print("ทำงานเสร็จสิ้น")
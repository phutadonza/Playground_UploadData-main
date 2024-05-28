# %%
# !pip3 install uptime-kuma-api

# %%
import time
import json
import uptime_kuma_api
from uptime_kuma_api.exceptions import UptimeKumaException
from uptime_kuma_api import UptimeKumaApi, MonitorType
# api = UptimeKumaApi('http://203.156.30.200')
api = UptimeKumaApi('http://10.94.12.132:3001')
api.login('multi', '@Multi.com')

# %%
# read csv
#import pandas as pd
#f = pd.read_csv('Kuma.csv', header=None)
#####data = pd.read_csv(r'C:\Users\Dell\Desktop\CCTV\Treading\CSV\CCTV-dt\CCTV-SYMC-RTC-13_148-out-dt.csv')

#print(len(data))
#for i in range (len(data)):
#    # name = data._get_value(i,'CAMERA_NAME')
#    name = data._get_value(i,'CAMERA_NAME')
#    sensor = data._get_value(i,'SENSOR_ID')
#    nvr = data._get_value(i,'NVR_IP')
#    api.add_monitor(
#        type=MonitorType.PING,
#        name=f"CAM : {name} : {nvr}",
#        hostname=nvr,
#        description=sensor,
#        resendInterval=5,
#        interval=30,
#        retryInterval=30
#    )
#    print(i,name,nvr,sensor)
print('login')
time.sleep(3)

#################################
#mes = api.get_monitors()
#    ###gomm = json.loads(json.dumps(mes[0]))
#    ####print(gomm['id'])
#####i = 1 
#id = []
#for i in mes:
#
#    #api.delete_monitor(i['id'])
#    nam = i['name'].split(' : ')
#    #print(len(nam))
#    if len(nam) >1:
#        #nam = i['name'].split(' : ')
#        print(nam[1])
#        #print(i['id'], i['name'])
#        #print(i['id'])
#        #print(i['name'])
#        #id.append(i['id'])
#    else:
#        print('len 0 ',i['name'])
#        
#
##print(id)
#time.sleep(30)
#print('Succes')
###################################################
    
#DELETE   #######################################
mes = api.get_monitors()
print(len(mes))
id = []
for i in mes:
    id.append(i['id'])
        
#print(id)
time.sleep(3)
print('Get Succes')

try:
    for j in id:        
        api.delete_monitor(j)
        print(j)
        #time.sleep(1)
except uptime_kuma_api.exceptions.Timeout as e:
    print(f"เกิดข้อผิดพลาด Timeout: {e}")


###################################################
#i= 1
#for i in range (200):
#    try:
#        mes = api.get_monitor(i)
#        #for x in mes:
#        #    print(x['id'],x['name'])
#        print(mes)
#    except UptimeKumaException as e:
#        print(i)
#        continue

###################################################


#try:
#    # Your code here
#    for i in range (614):        
#        api.delete_monitor(i)
#        
#         
#except UptimeKumaException as e:
#    if "monitor does not exist" in str(e):
#        print("Monitor does not exist. Handle accordingly.")
#    else:
#        print(f"Uptime Kuma API Exception: {e}")
        
######################################################



# %%
#for i in range(len(data)):
#    print(data._get_value(i,'CAMERA_NAME'))
#    for row, column in df.iterrows():
#        if data._get_value(i,'CAMERA_NAME') == column[0]:
#            print(column[0],'||', data._get_value(i,'CAMERA_NAME') )
            #api.add_monitor(
            #    type=MonitorType.PING,
            #    name=f"CAM : {column[0]} : {column[1]}",
            #    hostname=column[1],
            #    description=column[2],
            #    resendInterval=5,
            #    interval=30,
            #    retryInterval=30
            #)
#


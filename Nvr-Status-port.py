# %%
# !pip3 install uptime-kuma-api

# %%
import time 
from uptime_kuma_api.exceptions import UptimeKumaException, Timeout
from uptime_kuma_api import UptimeKumaApi, MonitorType
# api = UptimeKumaApi('http://203.156.30.200')


# %%
# read csv
import pandas as pd
#f = pd.read_csv('Kuma.csv', header=None)
data = pd.read_csv(r'C:\Users\Dell\Desktop\CCTV\Treading\CSV\CCTV-dt\Test.csv') 

print(len(data))


## THIS MAIN UP ONLY NOT CHECK DATA IN KUMA

# Your code here
for i in range (len(data)):
    
    name = data._get_value(i,'CAMERA_NAME')
    sensor = data._get_value(i,'SENSOR_ID')
    nvr = data._get_value(i,'NVR_IP')
    port = data._get_value(i,'NVR_IP')
    api = UptimeKumaApi('http://10.94.12.164:3001')
    api.login('multi','@Multi.com')

    
    try:
       
        api.add_monitor(
            type=MonitorType.PING,
            name=f"CAM : {name} : {nvr}",
            hostname=nvr,
            description=sensor,
            resendInterval=5,
            interval=30,
            retryInterval=30
        )
        print(name)
        #print(name)
        #time.sleep(10)
        
    except UptimeKumaException as e:
        print(i,name,nvr,sensor)
        if "monitor does not exist" in str(e):
            print("monitor does not exist")
            
        else:
            print(f"Uptime Kuma API Exception: {e}")
            
        #time.sleep(10)
            
time.sleep(30)
########################################################################

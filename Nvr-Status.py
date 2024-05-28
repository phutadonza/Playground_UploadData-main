# %%
# !pip3 install uptime-kuma-api

# %%
import time 
from uptime_kuma_api.exceptions import UptimeKumaException, Timeout
from uptime_kuma_api import UptimeKumaApi, MonitorType
# api = UptimeKumaApi('http://203.156.30.200')
api = UptimeKumaApi('http://10.94.12.164:3001')
api.login('multi','@Multi.com')

# %%
# read csv
import pandas as pd
#f = pd.read_csv('Kuma.csv', header=None)
data = pd.read_csv(r'C:\Users\Dell\Desktop\CCTV\Treading\CSV\CCTV-dt\Test.csv') 

print(len(data))



#for i in range (len(data)):
#    
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

################################################################################
## THIS MAIN UP ONLY NOT CHECK DATA IN KUMA

print('login')
time.sleep(5)
# Your code here
for i in range (len(data)):
    
    time.sleep(3)
    name = data._get_value(i,'CAMERA_NAME')
    sensor = data._get_value(i,'SENSOR_ID')
    nvr = data._get_value(i,'NVR_IP')
    
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
## CHECK DATA 
#
#print('login')
#time.sleep(3)
#mes = api.get_monitors()
#
#time.sleep(3)
#print(len(mes))
#
#def MES(data : str ) :
#
#    for i in mes:
#        nam = i['name'].split(' : ')
#        if len(nam) > 1: 
#
#            
#            if nam[1] == data:
#                
#                return nam[1]
#
#            
#            
#for j in range (len(data)):
#    
#    name = data._get_value(j,'CAMERA_NAME')
#    sensor = data._get_value(j,'SENSOR_ID')
#    nvr = data._get_value(j,'NVR_IP')
#    if name != MES(name):
#        print(name)
#    
#
#time.sleep(10)
#print('Succes')

##########################################################################
### CHECK DATA AND ADD
##
#print('login')
#time.sleep(3)
#mes = api.get_monitors()
#
#time.sleep(3)
#print(len(mes))
#
#def MES(data : str ) :
#
#    for i in mes:
#        nam = i['name'].split(' : ')
#        if len(nam) > 1: 
#
#            
#            if nam[1] == data:
#                
#                return nam[1]
#
#            
#            
#for j in range (len(data)):
#    
#    name = data._get_value(j,'CAMERA_NAME')
#    sensor = data._get_value(j,'SENSOR_ID')
#    nvr = data._get_value(j,'NVR_IP')
#    if name != MES(name):
#        print(name)
#        #try:
#        #    api.add_monitor(
#        #        type=MonitorType.PING,
#        #        name=f"CAM : {name} : {nvr}",
#        #        hostname=nvr,
#        #        description=sensor,
#        #        resendInterval=5,
#        #        interval=30,
#        #        retryInterval=30
#        #    )
#        #    time.sleep(10)
#        #    
#        #except UptimeKumaException as e:
#        #    if "monitor does not exist" in str(e):
#        #        print(i,name,nvr,sensor)
#        #    else:
#        #        print(f"Uptime Kuma API Exception: {e}")
#        
#    
#
#time.sleep(10)
#print('Succes')

########################################################################
## CHECK DATA AND Stop ALL
#
#
#print('login')
##time.sleep(3)
#
##mes = api.get_monitor(1)
##print(mes)
##api.pause_monitor(2)
##api.disconnect()
##api.pause_monitor(200)
####------
#mes = api.get_monitors()
#time.sleep(50)
#
#print(len(mes))
#
#for i in mes:
#    nam = i['name'].split(' : ')
#    if len(nam) > 1: 
#        while True:
#            try:
#                #print(i['id'])
#                api.pause_monitor(i['id'])
#                print( nam[1] )
#                time.sleep(2)
#                break
#            except Timeout as e:
#                print(f"Uptime Kuma API Timeout Exception: {e}")
#                continue
#
#            except UptimeKumaException as e:
#                print(f"Uptime Kuma API Exception: {e}")
#                continue
#
#            except Exception as e:
#                print(f"An unexpected error occurred: {e}")
#                continue
#            
#
#        
#api.disconnect()
#time.sleep(10)
#print('Succes')

########################################################################
#
### CHECK And Up Load
##
#print('login')
#time.sleep(3)
#mes = api.get_monitors()
#
#time.sleep(3)
#print(len(mes))
#    
#
#for i in mes:
#    arr  = []
#
#    nam = i['name'].split(' : ')
#    check = False
#    if len(nam) > 1: 
#
#        for j in range (len(data)):
#            name = data._get_value(j,'CAMERA_NAME')
#            sensor = data._get_value(j,'SENSOR_ID')
#            nvr = data._get_value(j,'NVR_IP')
#            
#            if nam[1] != name:
#                print( name) 
#                #print(name,nvr,sensor)
#                continue
#            
#            
#            #else :
#            #    print(name) 
#            #    
#            #    check = True
#            #    
#            #    if check == True:
#            #        #arr.append(name)
#            #        print( nam[1],name) 
#                
#                
#                #try:
#                #    api.add_monitor(
#                #        type=MonitorType.PING,
#                #        name=f"CAM : {name} : {nvr}",
#                #        hostname=nvr,
#                #        description=sensor,
#                #        resendInterval=5,
#                #        interval=30,
#                #        retryInterval=30
#                #    )
#                #    time.sleep(10)
#                #    
#                #except UptimeKumaException as e:
#                #    if "monitor does not exist" in str(e):
#                #        print(i,name,nvr,sensor)
#                #    else:
#                #        print(f"Uptime Kuma API Exception: {e}")
#  
#    else:
#        
#        print('len 1 ',i['name'])
#
##print(arr) 
#        
#
##print(id)
#time.sleep(10)
#print('Succes')


########################################################################
           

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


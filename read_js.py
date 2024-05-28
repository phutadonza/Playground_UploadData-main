import json

def get_js (name_obs):
    f = open(r'C:\Users\phutadon\OneDrive\Desktop\Playground_UploadData-main\cctv2-observedProp.json')

    data = json.load(f)

    for i in data['value']:
        #if i['name'] == 'RTSP-Live':
        if i['name'] == name_obs:        
            #print(i['name'],i["@iot.id"])
            return i["@iot.id"],i['name']

    f.close()


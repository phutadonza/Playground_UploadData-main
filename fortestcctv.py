import requests
import json
    
url = "http://cctv.naimueang.com:30800/core/api/streaming/v1.1/Observations"
    
payload = json.dumps({

  "result" : "",
  "resultType": "string",
  "Datastream":{"@iot.id":"664f091ce653d124cbed6e68"},

})
headers = {
  'Content-Type': 'application/json',
  'API-Key':'xhU0LHVN2QIZz1Dr4PKpOmUDQeJsi9qboQxX9oIdJqryffTVYOwlOblVSLJN1Z73'
}   
 
response = requests.request("POST", url, headers=headers, data=payload)
    
print(response.text)

import requests


url=f'https://bkk.larry-cctv.com/core/api/streaming/v1.1/FeaturesOfInterest'

headers = {
    'API-Key': 'k3hqivYfUBAEE7BoL1745jQE4PGS0Vq8CL755gMen1tm1shTatHSkyilgi1YnGGa',
    'Content-Type': 'application/json'
}

response = requests.get(url,headers=headers)

if(response.status_code == 200):
    print(response.json())
else:
    print(response.status_code)
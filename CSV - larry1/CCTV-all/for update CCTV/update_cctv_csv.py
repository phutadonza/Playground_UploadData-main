import requests
import csv
import os
import time

api_key = 'k3hqivYfUBAEE7BoL1745jQE4PGS0Vq8CL755gMen1tm1shTatHSkyilgi1YnGGa'
base_url = 'https://bkk.larry-cctv.com/core/api/streaming/v1.1/Things'
top = 10000
skip = 0
things_count = 10539
output_dir = r'C:\Users\phutadon\OneDrive\Desktop\Playground_UploadData-main\CSV - larry1\CCTV-all'
output_file = os.path.join(output_dir, 'things_data.csv')

# Function to get data from API
def get_things_data(skip, top):
    url = f"{base_url}?api_key={api_key}&$skip={skip}&$top={top}"
    response = requests.get(url)
    return response.json()

# Open CSV file for writing
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['iot.id', 'name'])  # Write header

    while skip < things_count:
        data = get_things_data(skip, top)
        for item in data['value']:
            writer.writerow([item['@iot.id'], item['name']])
        skip += top
        time.sleep(1)  # Delay for 1 second to avoid overloading the server

print(f"Data has been written to {output_file}")

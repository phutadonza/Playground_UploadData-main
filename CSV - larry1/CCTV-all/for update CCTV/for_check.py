import requests
import csv
import os
import time
import pandas as pd

api_key = 'k3hqivYfUBAEE7BoL1745jQE4PGS0Vq8CL755gMen1tm1shTatHSkyilgi1YnGGa'
base_url = 'https://bkk.larry-cctv.com/core/api/streaming/v1.1/Things'
top = 10000
skip = 0
things_count = 15000
output_dir = r'C:\Users\phutadon\OneDrive\Desktop\Playground_UploadData-main\CSV - larry1\CCTV-all'
output_file = os.path.join(output_dir, 'things_data.csv')
duplicates_file = os.path.join(output_dir, 'duplicates_data.csv')

# Function to get data from API
def get_things_data(skip, top):
    url = f"{base_url}?api_key={api_key}&$skip={skip}&$top={top}"
    response = requests.get(url)
    return response.json()

# Retrieve things data and save to CSV
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

# Read things data
things_df = pd.read_csv(output_file)

# Check for duplicate names
duplicate_names = things_df[things_df.duplicated('name', keep=False)]

# Save duplicates to a new CSV file
duplicate_names.to_csv(duplicates_file, index=False)

print(f"Duplicate data has been written to {duplicates_file}")

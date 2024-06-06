import requests
import csv
import os
import time
import pandas as pd

api_key = 'k3hqivYfUBAEE7BoL1745jQE4PGS0Vq8CL755gMen1tm1shTatHSkyilgi1YnGGa'
base_url = 'https://bkk.larry-cctv.com/core/api/streaming/v1.1/Things'
top = 10000
skip = 0
things_count = 10539
output_dir = r'C:\Users\phutadon\OneDrive\Desktop\Playground_UploadData-main\CSV - larry1\CCTV-all'
output_file = os.path.join(output_dir, 'things_data.csv')
compare_dir = r'C:\Users\phutadon\OneDrive\Desktop\Playground_UploadData-main\CSV - larry1\CCTV'

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

# Read all CSV files in compare_dir
comparison_files = [f for f in os.listdir(compare_dir) if f.endswith('.csv')]
matches = []

for comp_file in comparison_files:
    comp_file_path = os.path.join(compare_dir, comp_file)
    comp_df = pd.read_csv(comp_file_path)
    
    # Check for matching names
    for thing_name in things_df['name']:
        if thing_name in comp_df['POLE_NAME'].values:
            matches.append((thing_name, comp_file))

# Print matches
for match in matches:
    print(f"Match found: {match[0]} in file {match[1]}")

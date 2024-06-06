import csv
import requests
import json
import threading
from host.server import SERVER
from host.api import API
import os
import time
import pandas as pd

# Set Server in File host
top = 10000
skip = 0
things_count = 10539
output_dir = r'C:\Users\phutadon\OneDrive\Desktop\Playground_UploadData-main\CSV - larry1\CCTV-all'
output_file = os.path.join(output_dir, 'things_data.csv')
compare_dir = r'C:\Users\phutadon\OneDrive\Desktop\Playground_UploadData-main\CSV - larry1\CCTV'
check_before_up_dir = r'C:\Users\phutadon\OneDrive\Desktop\Playground_UploadData-main\CSV - larry1\CHECK BEFORE UP'

headers = {
    'API-Key': API,
    'Content-Type': 'application/json'
}

# Function to get data from API
def get_things_data(skip, top):
    url = f"{SERVER}/core/api/streaming/v1.1/Things?api_key={API}&$skip={skip}&$top={top}"
    response = requests.get(url)
    return response.json()

# Retrieve things data and save to CSV
def fetch_things_data():
    global skip
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

# Function to check for matching names
def check_matching_names(things_df, compare_dir):
    matches = []

    # Read all CSV files in compare_dir
    comparison_files = [f for f in os.listdir(compare_dir) if f.endswith('.csv')]

    for comp_file in comparison_files:
        comp_file_path = os.path.join(compare_dir, comp_file)
        comp_df = pd.read_csv(comp_file_path)

        # Check for matching names
        for thing_name in things_df['name']:
            if thing_name in comp_df['POLE_NAME'].values:
                matches.append((thing_name, comp_file))

    return matches

# Fetch things data
fetch_things_data()

# Read things data
things_df = pd.read_csv(output_file)

# Check for matching names and handle results
matches = check_matching_names(things_df, compare_dir)

# Save matches to new CSV file in CHECK BEFORE UP directory
if matches:
    match_file_path = os.path.join(check_before_up_dir, 'matched_pole_names.csv')
    with open(match_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['POLE_NAME', 'File'])  # Write header
        for match in matches:
            writer.writerow(match)
    print(f"Matches have been saved to {match_file_path}")

def createLocation(cctvDetail, headers):
    url = f"{SERVER}/core/api/streaming/v1.1/Locations"
    payload = json.dumps({
        "name": str(cctvDetail["POLE_NAME"]),
        "description": str(cctvDetail["POLE_DESCRIPTION"]),
        "encodingType": "application/vnd.geo+json",
        "location": {
            "type": "Point",
            "coordinates": [
                float(cctvDetail["LON"]),
                float(cctvDetail["LAT"])
            ]
        }
    })
    while True:
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 201:
            print("success with 201")
            break
        else:
            print("error occurred: %s" % response.text, response.json())
            continue 
    res_json = response.json()
    cctvDetail["LOCATION_ID"] = res_json["@iot.id"]
    return cctvDetail

def createThing(cctvDetail, location_id , headers):
    url = f"{SERVER}/core/api/streaming/v1.1/Things"
    payload = json.dumps({
        "name": str(cctvDetail["POLE_NAME"]),
        "description": str(cctvDetail["POLE_DESCRIPTION"]),
        "properties": {
            "lat": float(cctvDetail["LAT"]),
            "lon": float(cctvDetail["LON"])
        },
        "Locations": [
            {
                "@iot.id": location_id
            }
        ]
    })
    print("----- json =", payload)
    while True:
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 201:
            print("success with 201")
            break
        else:
            print("error occurred: %s" % response.text, response.json())
            continue
    res_json = response.json()
    cctvDetail["THING_ID"] = res_json["@iot.id"]
    return cctvDetail

def createFeatureOfInterest(cctvDetail , headers):
    url = f"{SERVER}/core/api/streaming/v1.1/FeaturesOfInterest"
    payload = json.dumps({
        "name": str(cctvDetail["POLE_NAME"]),
        "description": str(cctvDetail["POLE_DESCRIPTION"]),
        "encodingType": "application/vnd.geo+json",
        "feature": {
            "type": "Point",
            "coordinates": [
                float(cctvDetail["LON"]),
                float(cctvDetail["LAT"])
            ]
        }
    })
    while True:
        response = requests.request("POST", url, headers=headers, data=payload)
        if (response.status_code == 201):
            print("success with 201")
            break
        else:
            print("error occurred: %s" % response.text, response.json())
            continue
    res_json = response.json()
    print('vale form createFeatureOfInterest == ', res_json)
    cctvDetail["FEATUREOFINTEREST_ID"] = res_json["@iot.id"]
    return cctvDetail

dir_path = r'C:\\Users\\phutadon\\OneDrive\\Desktop\\Playground_UploadData-main\\CSV - larry1\\CCTV'

def Insert_pole():
    for path in os.listdir(dir_path):  #path
        if os.path.isfile(os.path.join(dir_path, path)):
            print('test', os.path.join(dir_path, path))  # ไว้เช็ค path

            out_dict = []  # CSV
            with open(os.path.join(dir_path, path), encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                count = 0
                prev_name = ''
                locationid = ''
                thingid = ''
                featureid = ''
                i = 1
                for row in csv_reader:
                    print("----- i =", i)

                    if row['POLE_NAME'] != prev_name:
                        prev_name = row['POLE_NAME']

                        # Check if POLE_NAME exists in things data
                        if row['POLE_NAME'] in things_df['name'].values:
                            # Save to CHECK BEFORE UP directory
                            match_file_path = os.path.join(check_before_up_dir, 'duplicates.csv')
                            with open(match_file_path, mode='a', newline='', encoding='utf-8') as file:
                                writer = csv.writer(file)
                                if os.path.getsize(match_file_path) == 0:
                                    writer.writerow(['POLE_NAME', 'LON', 'LAT'])  # Write header if file is empty
                                writer.writerow([row['POLE_NAME'], row['LON'], row['LAT']])
                            print(f"Duplicate found: {row['POLE_NAME']} not added.")
                            continue

                        # Create location
                        out = createLocation(row, headers)
                        locationid = out['LOCATION_ID']

                        # Create thing
                        out = createThing(out, locationid, headers)
                        thingid = out["THING_ID"]

                        # Create feature of interest
                        out = createFeatureOfInterest(out, headers)
                        featureid = out["FEATUREOFINTEREST_ID"]

                        out_dict.append(out)
                        count += 1
                    else:
                        out_dict.append(row)
                        out_dict[i-1]["LOCATION_ID"] = locationid
                        out_dict[i-1]["THING_ID"] = thingid
                        out_dict[i-1]["FEATUREOFINTEREST_ID"] = featureid
                        
                    i += 1
                
                print("-------- thing count = %d" % count)  # Run for end and show

            field_names = list(out_dict[0].keys())
            split_txt = os.path.join(dir_path, path).split('\\')
            name_text = split_txt[-1].split('.')
            file_save = f'C:\\Users\\phutadon\\OneDrive\\Desktop\\Playground_UploadData-main\\CSV - larry1\\CCTV-out\\{name_text[0]}-out.csv'
            completeName = os.path.join(file_save)
            with open(completeName, 'w', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=field_names)
                writer.writeheader()
                writer.writerows(out_dict)

# สร้าง Thread สำหรับแต่ละฟังก์ชัน
thread1 = threading.Thread(target=Insert_pole)

# เริ่มการทำงานของแต่ละ Thread
thread1.start()

# รอให้ Thread ทำงานเสร็จ
thread1.join()

print("ทำงานเสร็จสิ้น")

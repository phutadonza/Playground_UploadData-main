import csv
import requests
import time

# Path to your CSV file
csv_file_path = r'C:\Users\phuta\Desktop\Playground_UploadData-main\CSV - larry1\CCTV\Camera_In_Vallaris-Larry_BKK - Delete.csv'

# API details
api_url = 'https://bkk.larry-cctv.com/core/api/streaming/v1.1'  # Replace with your actual API endpoint
headers = {
    'API-Key': 'k3hqivYfUBAEE7BoL1745jQE4PGS0Vq8CL755gMen1tm1shTatHSkyilgi1YnGGa',  # Replace with your actual token if required
    'Content-Type': 'application/json'
}

# Read the CSV file
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    rows = list(reader)

# Create a list to store the information
check_list = []

for row in rows:
    pole_name = row['POLE_NAME']  # Adjust based on your CSV structure
    print(f"Processing pole: {pole_name}")

    # Get iot.id for Location
    location_response = requests.get(f'{api_url}/Locations?name={pole_name}', headers=headers)
    print(f'Location API response code: {location_response.status_code}')
    if location_response.status_code == 200:
        location_data = location_response.json()
        if location_data and 'value' in location_data and len(location_data['value']) > 0 and '@iot.id' in location_data['value'][0]:
            location_id = location_data['value'][0]['@iot.id']
            row['LOCATION_ID'] = location_id
            print(f"Found Location ID: {location_id}")

            # Get iot.id for Thing by pole_name
            thing_response = requests.get(f'{api_url}/Things?name={pole_name}', headers=headers)
            print(f'Thing API response code: {thing_response.status_code}')
            if thing_response.status_code == 200:
                thing_data = thing_response.json()
                if thing_data and 'value' in thing_data and len(thing_data['value']) > 0 and '@iot.id' in thing_data['value'][0]:
                    thing_id = thing_data['value'][0]['@iot.id']
                    row['THING_ID'] = thing_id
                    print(f"Found Thing ID: {thing_id}")
                else:
                    row['THING_ID'] = 'Not Found'
                    print("Thing ID Not Found")
            else:
                row['THING_ID'] = 'Error'
                print("Error retrieving Thing ID")
        else:
            row['LOCATION_ID'] = 'Not Found'
            row['THING_ID'] = 'Not Found'
            print("Location ID Not Found")
    else:
        row['LOCATION_ID'] = 'Error'
        row['THING_ID'] = 'Error'
        print("Error retrieving Location ID")
    
    check_list.append(row)

# Print the check list
print("\nCheck List:")
for row in check_list:
    print(f"POLE_NAME: {row['POLE_NAME']}, LOCATION_ID: {row['LOCATION_ID']}, THING_ID: {row['THING_ID']}")

# Ask user for confirmation to delete
user_input = input("\nDo you want to delete all listed Things and Locations? Type 'delete' to confirm: ")
if user_input.lower() == 'delete':
    for row in check_list:
        if row['THING_ID'] not in ['Not Found', 'Error']:
            delete_response = requests.delete(f'{api_url}/Things({row["THING_ID"]})', headers=headers)
            if delete_response.status_code in [200, 204]:
                print(f"Thing with ID {row['THING_ID']} for pole {row['POLE_NAME']} deleted successfully.")
            elif delete_response.status_code == 404:
                print(f"Thing with ID {row['THING_ID']} for pole {row['POLE_NAME']} not found. It might have been already deleted.")
            else:
                print(f"Failed to delete Thing with ID {row['THING_ID']} for pole {row['POLE_NAME']}. Status code: {delete_response.status_code}")
                print(delete_response.text)
            time.sleep(1)  # Delay for 1 second
        
        if row['LOCATION_ID'] not in ['Not Found', 'Error']:
            delete_response = requests.delete(f'{api_url}/Locations({row["LOCATION_ID"]})', headers=headers)
            if delete_response.status_code in [200, 204]:
                print(f"Location with ID {row['LOCATION_ID']} for pole {row['POLE_NAME']} deleted successfully.")
            elif delete_response.status_code == 404:
                print(f"Location with ID {row['LOCATION_ID']} for pole {row['POLE_NAME']} not found. It might have been already deleted.")
            else:
                print(f"Failed to delete Location with ID {row['LOCATION_ID']} for pole {row['POLE_NAME']}. Status code: {delete_response.status_code}")
                print(delete_response.text)
            time.sleep(1)  # Delay for 1 second
else:
    print("Deletion process aborted.")

import csv
import subprocess
import os

def test_camera_links(directory):
    csv_files = [file for file in os.listdir(directory) if file.endswith('.csv')]
    results = []

    for csv_file in csv_files:
        file_path = os.path.join(directory, csv_file)
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                link = row.get('NVR RTSP MAIN')
                if link:
                    try:
                        # Run VLC with the link
                        process = subprocess.Popen(f'vlc --intf dummy --play-and-exit {link}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                        stdout, stderr = process.communicate()
                        return_code = process.returncode

                        if return_code == 0:
                            results.append((link, 'Accessible'))
                        else:
                            results.append((link, 'Inaccessible'))
                    except Exception as e:
                        results.append((link, 'Error: ' + str(e)))

    return results

# Specify the directory path where CSV files are located
directory = r'C:\Users\phutadon\OneDrive\Desktop\Playground_UploadData-main\CSV - larry1\CCTV'
results = test_camera_links(directory)

# Print the results
for link, status in results:
    print(f'{link}: {status}')

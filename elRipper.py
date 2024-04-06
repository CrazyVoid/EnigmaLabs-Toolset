#!/usr/bin/python3
import sys, os, struct
import random, time
import argparse
import requests


baseurl = "https://enigmalabs.io/incident/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
failed_reports = []

skip_delay = 0

def download_html(url, num, output_folder):
    global skip_delay
    try:
        # Send a GET request to the URL
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            html_content = response.text
            
            content_type = response.headers['Content-Type']
            content_length = response.headers.get('Content-Length', 'Not specified')
            print("[INFO] Content-Type:" + content_type + " - Content Length: " + content_length)

            # save content to file
            with open(output_folder + '/' + str(num) + '.html', 'w', encoding='utf-8') as file:
                 file.write(html_content)
            print('[INFO] Saved Incident Report #' + str(num) + ' To ' + output_folder + '/' + str(num) + '.html')
            print('[INFO] Size of Response : ' + str(sys.getsizeof(response)) + ' Bytes')

        else:
            print(f"[Error] Failed to retrieve incident #"+str(num)+". Status code: " + str(response.status_code))
            failed_reports.append(num)
            skip_delay = 1

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Check if the script is run with the correct number of command-line arguments
    if len(sys.argv) != 4:
        print("Usage: python elRipper.py <start_number> <end_number> <output_dir>")
        sys.exit(1)

    print('[SCRIPT] EngimaLabs Incident Report Html Ripper v1.2 - Crazyvoid\n')
    # Get the number from the command-line argument
    start_num = int(sys.argv[1])
    end_num = int(sys.argv[2])
    output_dir = sys.argv[3]


    if(start_num < 0):
        print('[ERROR] start_num {' + str(start_num) + '} must be above 0')
        sys.exit(2)

    if(start_num > end_num or end_num < start_num):
        print('[ERROR] start_num {' + str(start_num) + '} must not be greater then ' + str(end_num))
        sys.exit(3)

    if not os.path.exists(output_dir):
        # If it doesn't exist, create the folder
        os.makedirs(output_dir)
        print(f"[SYSTEM] Folder '{output_dir}' created successfully.")
    
    
    # vars needed for script
    report_count = 0
    delay_count = 0
    start_script_time = time.time()
    range_end = end_num + 1

    for num in range(start_num, range_end):
        # Download the report
        print('[INFO] Downloading Incinident #' + str(num))
        download_html(baseurl + str(num), num, output_dir)
        
        # Increment the counters
        report_count = report_count + 1
        delay_count = delay_count + 1

        if skip_delay == 0:
            # Setting an short delay between each report download to make it look more human
            calc_delay = random.uniform(1, 5)
            print("[INFO] Delay of {} seconds\n".format(calc_delay))
            time.sleep(calc_delay)
        else:
            skip_delay = 0
            print('[INFO] skipping report delay\n')
        

        # Setting an long delay after 100 reports between 3 to 4 mins to make it look more human
        if(delay_count == 100):
            calc_long_delay = random.uniform(60,120)
            print('\n[INFO] Long Delay after 100 Reports - ' + str(calc_long_delay) + ' Seconds\n')
            time.sleep(calc_long_delay)
            delay_count = 0

    # Calc the time it took for the script to run
    end_script_time = time.time()
    elapsed_script_time = end_script_time - start_script_time

    print('\n\n[INFO] Script Finished with ' + str(report_count) + ' Incident Reports Downloaded\n')
    print('[INFO] It took ' + str(elapsed_script_time) + ' seconds to run the script!\n')
    print(f"[INFO] Failed to download incidents: {failed_reports}")
#!/usr/bin/python3
import sys
import os
import re
import time
import csv
from bs4 import BeautifulSoup

# List to store CSV data
csv_datalist = [['ID', 'DATE', 'TIME', 'GPS', 'DURATION', 'SHAPE', 'GEO', 'REPORT', 'EXT_DATA', 'EXT_DATE_TYPE', 'ORIG_FILEPATH']]

def generate_html_filelist(dir_path):
    """Generate a list of HTML files in the given directory."""
    html_files = []
    for tmp_filename in os.listdir(dir_path):
        tmp_filepath = os.path.join(dir_path, tmp_filename)
        if os.path.isfile(tmp_filepath) and tmp_filename.lower().endswith('.html'):
            html_files.append(tmp_filepath)
    return html_files

def remove_html_tags(html):
    """Remove HTML tags from the given HTML content."""
    try:
        soup = BeautifulSoup(html, 'html.parser')
        text_content = soup.get_text(separator=' ', strip=True)
        text_content = re.sub(r'\s+', ' ', text_content)
        return text_content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def extract_date_time(html_content):
    """Extract date and time from the given HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    date_time_tag = soup.find('p', class_='text-gray-medium font-monument mb-2')
    
    if date_time_tag:
        date_time_text = date_time_tag.get_text(strip=True)
        return date_time_text
    
    return None

def extract_card_data(input_string):
    """Extract card data from the given input string."""
    parts = input_string.split()
    location = None
    duration = None
    shape = None
    for i in range(len(parts)):
        if parts[i] == "Location" and i + 2 < len(parts):
            latitude = float(parts[i + 1][1:-1])
            longitude = float(parts[i + 2][:-1])
            location = (latitude, longitude)
        elif parts[i] == "Duration" and i + 1 < len(parts):
            duration = parts[i + 1]
        elif parts[i] == "Shape" and i + 1 < len(parts):
            shape = parts[i + 1]
    return location, duration, shape

def process_html_file(input_dump_file):
    """Process HTML file and extract relevant data."""
    print('[INFO] Opening Dump File : ' + input_dump_file)
    fileHandle = open(input_dump_file, 'r', encoding='utf-8')
    fileSize = os.path.getsize(input_dump_file)
    fileContent = fileHandle.read()
    print('[INFO] File Size : ' + str(fileSize))
    cleanSoup = remove_html_tags(fileContent)
    soup = BeautifulSoup(fileContent, 'html.parser')
    
    # Extracting Witness count
    witcountdiv = soup.find('p', class_='tracking-widest')
    if witcountdiv:
        witcountdiv_content = witcountdiv.get_text(separator=' ', strip=True)
        witcountdiv_content = witcountdiv_content.replace('Witnesses ', '', 1)
        print('[DUMP] Witnesses (' + witcountdiv_content + ')')
    else:
        witcountdiv_content = '0'
        print('[DUMP] Witnesses (' + witcountdiv_content + ') - failed to get value - default : 0')
    
    # Extracting Date and Time
    datetimefr = extract_date_time(fileContent)

    if datetimefr:
        if "•" in datetimefr:
            datetimefr = datetimefr.replace("•", "&")
            print(datetimefr)
            mydate, mytime = datetimefr.split('&')
        elif "â¢" in datetimefr:
            datetimefr = datetimefr.replace("â¢", "&")
            mydate, mytime = datetimefr.split('&')
        else:
            print('[UKNOWN] hit unknown point 000x1')
            mydate, mytime = 'NULL', 'NULL'
        print('[DUMP] Date Time : ' + datetimefr)
    else:
        mydate = 'NULL'
        mytime = 'NULL'
        print('[DUMP] Date Time - failed to dump (NULL)')
    
    # Extracting Card Info
    carddiv = soup.find('div', class_='shape-card-container')
    if carddiv:
        carddiv_content = carddiv.get_text(separator=' ', strip=True)
        card_gps, card_duration, card_shape = extract_card_data(carddiv_content)
        print('[DUMP] Card Info : ' + carddiv_content)
    else:
        carddiv_content = 'NULL'
        card_gps, card_duration, card_shape = 'NULL', 'NULL', 'NULL'
        print('[DUMP] Card Info : failed to get data - default : NULL')
    
    # Extracting Geo
    geodiv = soup.find('h2', class_='tracking-widest')
    if geodiv:
        geodiv_content = geodiv.get_text(separator=' ', strip=True)
        print('[DUMP] Geo : ' + geodiv_content)
    else:
        geodiv_content = 'NULL'
        print('[DUMP] Geo : failed to get data - default : ' + geodiv_content)
    
    # Extracting Report
    reportdiv = soup.find('p', class_='text-base')
    if(reportdiv):
        reportdiv_content = reportdiv.get_text(separator=' ', strip=True)
        reportdiv_size = len(reportdiv_content)
        print('[Dump] Report[size:'+str(reportdiv_size)+'] : '+ reportdiv_content[:60] + '\n')
    else:
        reportdiv_content = 'NULL'
        print('[Dump] Report : failed to get data - default : '+ reportdiv_content + '\n')
    
    # Close the file handle
    fileHandle.close()
    
    # Adding data to CSV list
    report_num = os.path.basename(input_dump_file).replace('.html', '')
    tmp_list = [report_num, mydate, mytime, card_gps, card_duration, card_shape, geodiv_content, reportdiv_content, 'NULL', 'NULL', input_dump_file]
    csv_datalist.append(tmp_list)

def write_csv(data, file_path):
    """Write CSV data to the given file."""
    with open(file_path, mode='w+', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

if __name__ == "__main__":
    # Check if the script is run with the correct number of command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python elHtml2Csv.py <input_dump_dir> <output_csv_file>")
        sys.exit(1)

    start_script_time = time.time()
    print('\nEnigmaLabs Dumped HTML to CSV Converter v1 - Crazyvoid\n')

    # Get the vars needed
    input_dump_dir = sys.argv[1]
    output_csv_file = sys.argv[2]
    print('Arg[input_dump_dir]  : ' + input_dump_dir)
    print('Arg[output_csv_file] : ' + output_csv_file + '\n')

    if os.path.exists(input_dump_dir) and os.path.isdir(input_dump_dir):
        if os.path.exists(output_csv_file):
            print('[ERROR] output csv file : ' + output_csv_file + ' - Already exist, Please select an new output filename!')
            sys.exit(3)
        else:
            dir_filelist = generate_html_filelist(input_dump_dir)
            if dir_filelist:
                num_html_files = len(dir_filelist)
                print('[INFO] ' + str(num_html_files) + ' html files in input dump directory!')
                for x_file in dir_filelist:
                    process_html_file(x_file)
                print('[INFO] Writing CSV File : ' + output_csv_file)
                write_csv(csv_datalist, output_csv_file)
            else:
                print('[ERROR] input dump directory contains no html files!')
                sys.exit(4)
    else:
        print('[ERROR] input dump directory : ' + input_dump_dir + ' - Does not exist!')
        sys.exit(2)

    end_script_time = time.time()
    elapsed_script_time = end_script_time - start_script_time
    print('[INFO] It took ' + str(elapsed_script_time) + ' seconds to run the script!\n')
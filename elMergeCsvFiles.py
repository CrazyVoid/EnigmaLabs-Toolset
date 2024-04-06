#!/usr/bin/python3
import sys, os, time, argparse, csv

def read_csv(file_path):
    """Read data from a CSV file and return it as a list of lists."""
    data = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        # Skip header
        next(reader)
        for row in reader:
            data.append(row)
    return data

def merge_and_sort_csv(file1_path, file2_path, output_file):
    """Merge and sort data from two CSV files by ID column and write to a new CSV file."""
    # Read data from both CSV files
    data1 = read_csv(file1_path)
    data2 = read_csv(file2_path)
    
    # Merge data from both files
    merged_data = data1 + data2
    
    # Sort merged data by ID (assuming ID is the first column)
    sorted_data = sorted(merged_data, key=lambda x: int(x[0]))
    
    # Write sorted data to a new CSV file
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(['ID', 'DATE', 'TIME', 'GPS', 'DURATION', 'SHAPE', 'GEO', 'REPORT', 'EXT_DATA', 'EXT_DATE_TYPE', 'ORIG_FILEPATH'])
        writer.writerows(sorted_data)

if __name__ == "__main__":
    start_script_time = time.time()
    # Check if the script is run with the correct number of command-line arguments
    if len(sys.argv) != 4:
        print("Usage: python elMergeCsvFiles.py <first_input_csv> <second_input_csv> <merged_output_csv>")
        sys.exit(1)

    file1_path = sys.argv[1]
    file2_path = sys.argv[2]
    output_file = sys.argv[3]

    if not os.path.exists(file1_path):
        print('[ERROR] first_input_csv : ' + file1_path + ' - File does not exist!\n')
        sys.exit(2)

    if not os.path.exists(file2_path):
        print('[ERROR] second_input_csv : ' + file2_path + ' - File does not exist!\n')
        sys.exit(2)

    if os.path.exists(output_file):
        print('[ERROR] merged_output_csv : ' + output_file + ' - Already exist!\n')

    merge_and_sort_csv(file1_path, file2_path, output_file)
    print(f"[INFO] Merged csv and sorted data saved to '{output_file}'.")

    # Calc the time it took for the script to run
    end_script_time = time.time()
    elapsed_script_time = end_script_time - start_script_time
    print('[INFO] It took ' + str(elapsed_script_time) + ' seconds to run the script!\n')
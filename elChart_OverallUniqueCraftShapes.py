#!/usr/bin/python3
import sys, os, argparse, time
import pandas as pd
import matplotlib.pyplot as plt

def plot_shape_counts(csv_file, output_chart_image):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Count the occurrences of each unique shape
    shape_counts = df['SHAPE'].value_counts()
    
    # Plot the counts
    plt.figure(figsize=(10, 6))
    shape_counts.plot(kind='bar', color='skyblue')
    plt.title('Count of Each Unique Shape')
    plt.xlabel('Shape')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Save the chart image
    plt.savefig(output_chart_image)
    plt.close()


if __name__ == "__main__":
    start_script_time = time.time()
    # Check if the script is run with the correct number of command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python elRipper.py <input_csv_file> <output_chart_image>")
        sys.exit(1)

    input_csv_file = sys.argv[1]
    output_chart_image = sys.argv[2]

    plot_shape_counts(input_csv_file, output_chart_image)

    # Calc the time it took for the script to run
    end_script_time = time.time()
    elapsed_script_time = end_script_time - start_script_time
    print('[INFO] It took ' + str(elapsed_script_time) + ' seconds to run the script!\n')

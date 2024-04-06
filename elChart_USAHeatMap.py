import argparse, re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import warnings

us_pattern = r'\b(?:United States|USA)\b|\b[A-Z][a-z\s]*,\s*[A-Z]{2}\b'
specific_shape_set = "NULL"
specific_daterange_set = "NULL"
specific_amount_of_records = 0
specific_total_db_rows = 0
specific_db_name = "NULL"

def read_csv_data(csv_file, output_png, date_time_range=None, specific_shape=None):
    global specific_total_db_rows, specific_db_name  # Declare the variable as global

    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Get the number of rows returned after filtering
    num_rows = df.shape[0]
    specific_total_db_rows = num_rows  # Update the global variable
    print("Number of rows returned:", num_rows)

    specific_db_name = csv_file

    df = df[df['GEO'].str.contains(us_pattern, na=False, flags=re.IGNORECASE)]

    # Parse date
    df['DATE'] = pd.to_datetime(df['DATE'], format='mixed', errors='coerce').dt.date

    #print('Example of dates ===================================')
    #print(df['DATE'].head(10))

    # Filter DataFrame based on date-time range if provided
    if date_time_range:
        print('Start Date : ' + str(date_time_range[0]))
        print('End Date : ' + str(date_time_range[1]))
        start_date, end_date = pd.to_datetime(date_time_range[0]).date(), pd.to_datetime(date_time_range[1]).date()
        df = df[(df['DATE'] >= start_date) & (df['DATE'] <= end_date)]

    # Filter DataFrame based on specific shape if provided
    if specific_shape:
        df = df[df['SHAPE'] == specific_shape]
        
    # Extract GPS coordinates from the 'GPS' column
    df['GPS'] = df['GPS'].str.strip('()')  # Remove brackets
    
    #df[['Longitude', 'Latitude']] = df['GPS'].str.strip('-').str.split(',', expand=True).astype(float)
    df[['Longitude', 'Latitude']] = df['GPS'].str.split(',', expand=True).astype(float)

    # Swap latitude and longitude
    latitudes = df['Longitude'].values
    longitudes = df['Latitude'].values

    return latitudes, longitudes

def plot_heatmap_on_us_map(output_png, latitudes, longitudes, input_gridsize, input_cmap_value, input_geo_outline_color):
    # Create a new figure
    fig = plt.figure(figsize=(10, 6))

    # Create a map with the desired projection (e.g., Lambert Conformal)
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    # Calculate the bounding box based on the latitude and longitude coordinates
    min_lon, max_lon = min(longitudes), max(longitudes)
    min_lat, max_lat = min(latitudes), max(latitudes)

   # Create a map with the desired projection (e.g., Lambert Conformal)
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.LambertConformal())
    ax.set_extent([-125, -65, 24, 50], crs=ccrs.PlateCarree())  # Set custom extent for US

    # Plot heatmap
    hb = ax.hexbin(longitudes, latitudes, gridsize=input_gridsize, cmap=input_cmap_value, transform=ccrs.PlateCarree(), zorder=1)

    # Load the map outline for the US
    ax.add_feature(cfeature.COASTLINE.with_scale('10m'), zorder=2, color=input_geo_outline_color, linewidth=2)

    # Add state outlines
    states_provinces = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces_lines',
        scale='50m',
        facecolor='none')
    ax.add_feature(states_provinces, edgecolor=input_geo_outline_color, linewidth=2)

    # Add country borders
    ax.add_feature(cfeature.BORDERS, edgecolor=input_geo_outline_color, linewidth=2, linestyle=':', zorder=3)

    # Add colorbar
    plt.colorbar(hb, ax=ax, label='Density')

    # Add title
    plt.title('Heatmap of GPS Coordinates across the United States')

    if not specific_shape_set == "NULL":
        ss_text = "UFO Shape : " + specific_shape_set
        plt.text(0.95, 0.05, ss_text, horizontalalignment='right', verticalalignment='bottom', transform=fig.transFigure)

    if not specific_daterange_set == "NULL":
        plt.text(0.05, 0.05, specific_daterange_set, horizontalalignment='left', verticalalignment='bottom', transform=fig.transFigure)

    if not len(latitudes) == 0:
        plt.text(0.95, 0.92, "Total Database Records : " + str(specific_total_db_rows), horizontalalignment='right', verticalalignment='top', transform=fig.transFigure)
        plt.text(0.95, 0.95, "Records Used for Rendering : " + str(len(latitudes)), horizontalalignment='right', verticalalignment='top', transform=fig.transFigure)

    plt.text(0.95, 0.02, "Database File : " + specific_db_name, horizontalalignment='right', verticalalignment='bottom', transform=fig.transFigure)

    # Print some information about the data
    print("Number of data points used:", len(latitudes))

    # Save the plot as PNG
    plt.savefig(output_png, dpi=300)
    print('[INFO] Saved output image : ' + output_png)

    # Show the plot
    plt.show()

if __name__ == "__main__":
    print('[APP] EngimaLabs USA Heatmap Generator v1.3 - Crazyvoid\n')
    parser = argparse.ArgumentParser(description='Generate heatmap of GPS coordinates across the United States.')
    parser.add_argument('csv_file', type=str, help='Path to the CSV file containing GPS coordinates and other data.')
    parser.add_argument('--output_png', type=str, default='heatmap_on_us_map.png', help='Output PNG file path')
    parser.add_argument('--start_date', type=str, help='Start date for filtering CSV Data (YYYY-MM-DD)')
    parser.add_argument('--end_date', type=str, help='End date for filtering CSV Data (YYYY-MM-DD)')
    parser.add_argument('--specific_shape', type=str, help='Specific shape for filtering CSV Data')
    parser.add_argument('--grid_size', type=int, default=50, help='Size of the heatmap grids (bigger is smaller heatmap dots) default:50')
    parser.add_argument('--cmap', type=str, default='coolwarm', help='The selected colormap mode (default:coolwarm)')
    parser.add_argument('--outline_color', type=str, default='black', help='The color to use for the geographical outlines. (default:black)')

    args = parser.parse_args()

    # remove small warnings
    warnings.filterwarnings("ignore", message=".*")

    date_time_rangex = None
 #   if args.start_date and args.end_date:
 #       date_time_rangex = (args.start_date, args.end_date)
 #       specific_daterange_set = "Date Range : " + str(date_time_rangex)

    if args.specific_shape:
        specific_shape_set = args.specific_shape

    # Read GPS data from CSV
    latitudes, longitudes = read_csv_data(args.csv_file, args.output_png, date_time_range=date_time_rangex, specific_shape=args.specific_shape)

    # Plot heatmap on US map
    plot_heatmap_on_us_map(args.output_png, latitudes, longitudes, args.grid_size, args.cmap, args.outline_color)


# NOTES
# - Need to work on the date range stuff, many errors happen
# - Clean up the code and comment it to.
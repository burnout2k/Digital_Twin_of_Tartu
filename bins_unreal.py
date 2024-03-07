""" Using the projection string converts the WSG coordinates to the ones usable in Unreal Engine's scene """

import csv
import pyproj

def wgs_to_unreal(lat, lon):
    proj = pyproj.Proj('+proj=tmerc +lat_0=58.382296 +lon_0=26.726196 +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m +vunits=m +no_defs')
    x, y = proj(lon, lat)
    y = -y  # Flip Y-axis
    return x, y

# Paths for the input and output CSV files
input_csv_file = "/home/allan/carla/Unreal/CarlaUE4/Content/Carla/Maps/tartu_large/scripts/bins_clean.csv"
output_csv_file = "/home/allan/carla/Unreal/CarlaUE4/Content/Carla/Maps/tartu_large/scripts/bins_unreal.csv"

temp_rows = []

# Read the input file
with open(input_csv_file, mode='r') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        lon, lat = float(row['X']), float(row['Y'])
        x, y = wgs_to_unreal(lat, lon)
        row['X'], row['Y'] = x, y
        temp_rows.append(row)

# Write to the output file
with open(output_csv_file, mode='w', newline='') as outfile:
    fieldnames = temp_rows[0].keys()
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in temp_rows:
        writer.writerow(row)

print(f"Coordinates updated and saved to {output_csv_file}.")



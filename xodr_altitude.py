""" Adds altitude to OpenDRIVE file. """

import rasterio
import pyproj
from functools import partial
from shapely.geometry import Point
from shapely.ops import transform
from rasterio.transform import rowcol
import numpy as np
from xml.etree import ElementTree as ET

def read_raster(file_path):
    with rasterio.open(file_path) as src:
        data = src.read(1)
        transform = src.transform
    return data, transform

def read_rasters(file_paths):
    return [read_raster(file_path) for file_path in file_paths]

def parse_opendrive(file_path):
    tree = ET.parse(file_path)
    road_coordinates = {}
    for road in tree.findall('road'):
        road_id = road.get('id')
        road_coordinates[road_id] = [(float(geom.get('x')), float(geom.get('y')))
                                     for geom in road.findall('.//geometry')]
    return road_coordinates

def transform_coordinates(coordinates, source_crs, destination_crs):
    transformer = pyproj.Transformer.from_crs(source_crs, destination_crs, always_xy=True)
    return [transformer.transform(coord[0], coord[1]) for coord in coordinates]

def determine_correct_raster(road_coords, rasters):
    for raster_data, raster_transform in rasters:
        try:
            row, col = rowcol(raster_transform, road_coords[0][0], road_coords[0][1])
            if 0 <= row < raster_data.shape[0] and 0 <= col < raster_data.shape[1]:
                return raster_data, raster_transform
        except IndexError:
            continue
    return None, None

def sample_elevation_for_road(road_coords, raster_data, transform):
    elevations = []
    for coord in road_coords:
        row, col = rowcol(transform, coord[0], coord[1])
        if 0 <= row < raster_data.shape[0] and 0 <= col < raster_data.shape[1]:
            elevation = raster_data[row, col]
            elevations.append(elevation)
        else:
            elevations.append(None)
    return elevations

def add_sampled_elevation_to_roads(content, road_elevations):
    root = ET.fromstring(content)
    for road in root.findall('road'):
        road_id = road.get('id')
        if road_id in road_elevations:
            elevation_profile_elem = ET.Element('elevationProfile')
            for i, elevation in enumerate(road_elevations[road_id]):
                if elevation is not None:
                    elevation_elem = ET.SubElement(elevation_profile_elem, 'elevation')
                    elevation_elem.set('s', str(i))
                    elevation_elem.set('a', str(elevation))
                    elevation_elem.set('b', '0.0')
                    elevation_elem.set('c', '0.0')
                    elevation_elem.set('d', '0.0')
            existing_profile = road.find('elevationProfile')
            if existing_profile is not None:
                road.remove(existing_profile)
            road.append(elevation_profile_elem)
    return ET.tostring(root, encoding='unicode')

# File names
raster_file_names = ['54654_DTM_1m.tif', '54663_DTM_1m.tif', '54752_DTM_1m.tif',
                     '54754_DTM_1m.tif', '54761_DTM_1m.tif', '54763_DTM_1m.tif']
opendrive_file_name = 'tartu_large.xodr'

# Read raster files
rasters = read_rasters(raster_file_names)
road_coordinates = parse_opendrive(opendrive_file_name)

# Coordinate systems
source_crs = pyproj.CRS.from_proj4('+proj=tmerc +lat_0=58.382296 +lon_0=26.726196 +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs')
destination_crs = pyproj.CRS.from_epsg(3301)  # Estonian Coordinate System of 1997

# Process each road
transformed_road_elevations = {}
for road_id, coords in road_coordinates.items():
    transformed_coords = transform_coordinates(coords, source_crs, destination_crs)
    raster_data, raster_transform = determine_correct_raster(transformed_coords, rasters)
    if raster_data is not None:
        elevations = sample_elevation_for_road(transformed_coords, raster_data, raster_transform)
        transformed_road_elevations[road_id] = elevations

# Update OpenDRIVE file
with open(opendrive_file_name, 'r') as file:
    opendrive_content = file.read()

modified_opendrive_content = add_sampled_elevation_to_roads(opendrive_content, transformed_road_elevations)

# Save modified file
modified_opendrive_file_name = 'tartu_large_with_elevation.xodr'
with open(modified_opendrive_file_name, 'w') as file:
    file.write(modified_opendrive_content)

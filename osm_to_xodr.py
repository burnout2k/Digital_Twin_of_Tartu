""" Convert OpenStreetMap file to OpenDRIVE file. """

import argparse
import glob
import os
import sys

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla


def convert(args):
    # Read the .osm data
    with open(args.input_path, mode="r", encoding="utf-8") as osmFile:
        osm_data = osmFile.read()

    # Define the desired settings
    settings = carla.Osm2OdrSettings()

    # Set OSM road types to export to OpenDRIVE
    settings.set_osm_way_types([
        "motorway",
        "motorway_link",
        "trunk",
        "trunk_link",
        "primary",
        "primary_link",
        "secondary",
        "secondary_link",
        "tertiary",
        "tertiary_link",
        "unclassified",
        "residential"
    ])
    settings.default_lane_width = args.lane_width
    settings.generate_traffic_lights = args.traffic_lights
    settings.all_junctions_with_traffic_lights = args.all_junctions_lights
    settings.center_map = args.center_map
    settings.proj_string = '+proj=tmerc +lat_0=58.382296 +lon_0=26.726196 +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m +vunits=m +no_defs'

    # Convert to .xodr
    xodr_data = carla.Osm2Odr.convert(osm_data, settings)

    # save opendrive file
    with open(args.output_path, "w", encoding="utf-8") as xodrFile:
        xodrFile.write(xodr_data)

# ==============================================================================
# -- main() --------------------------------------------------------------------
# ==============================================================================


def main():
    argparser = argparse.ArgumentParser(
        description=__doc__)
    argparser.add_argument(
        '-i', '--input-path',
        required=True,
        metavar='OSM_FILE_PATH',
        help='set the input OSM file path')
    argparser.add_argument(
        '-o', '--output-path',
        required=True,
        metavar='XODR_FILE_PATH',
        help='set the output XODR file path')
    argparser.add_argument(
        '--lane-width',
        default=3.5,
        help='width of each road lane in meters')
    argparser.add_argument(
        '--traffic-lights',
        action='store_true',
        help='enable traffic light generation from OSM data')
    argparser.add_argument(
        '--all-junctions-lights',
        action='store_true',
        help='set traffic lights for all junctions')
    argparser.add_argument(
        '--center-map',
        action='store_true',
        help='set center of map to the origin coordinates')

    if len(sys.argv) < 2:
        argparser.print_help()
        return

    args = argparser.parse_args()

    if args.input_path is None or not os.path.exists(args.input_path):
        print('input file not found.')
    if args.output_path is None:
        print('output file path not found.')

    print(__doc__)

    try:
        convert(args)
    except:
        print('\nAn error has occurred in conversion.')


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')
    except RuntimeError as e:
        print(e)

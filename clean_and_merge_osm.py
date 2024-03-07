""" Combines different OpenStreetMap files into one and removes everything besides roads  """

import os
import glob
from xml.etree import ElementTree as ET

def clean_osm(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Find nodes related to main roads and residential roads
    road_nodes = set()
    for elem in root.findall("./*"):
        if elem.tag == "way":
            highway = None
            for tag in elem.findall("tag"):
                if tag.attrib["k"] == "highway":
                    highway = tag.attrib["v"]
                    break
            if highway and highway in ["motorway", "trunk", "primary", "secondary", "tertiary", "residential"]:
                for nd in elem.findall("nd"):
                    road_nodes.add(nd.attrib["ref"])

    # Remove all elements except roads, road bounds, and road nodes
    for elem in root.findall("./*"):
        if elem.tag == "node":
            if elem.attrib["id"] not in road_nodes:
                root.remove(elem)
            continue

        if elem.tag == "way":
            highway = None
            for tag in elem.findall("tag"):
                if tag.attrib["k"] == "highway":
                    highway = tag.attrib["v"]
                    break
            if not highway or highway not in ["motorway", "trunk", "primary", "secondary", "tertiary", "residential"]:
                root.remove(elem)
        else:
            root.remove(elem)

    tree.write(output_file, encoding="UTF-8", xml_declaration=True)

def merge_osm_files(input_files, output_file):
    new_root = None

    for input_file in input_files:
        tree = ET.parse(input_file)
        root = tree.getroot()

        if new_root is None:
            new_root = ET.Element("osm", root.attrib)

        for elem in root.findall("./*"):
            if elem.tag in ["node", "way"]:
                new_root.append(elem)

    new_tree = ET.ElementTree(new_root)
    new_tree.write(output_file, encoding="UTF-8", xml_declaration=True)

def remove_duplicates(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    unique_nodes = {}
    unique_ways = {}

    for elem in root.findall("./*"):
        if elem.tag == "node":
            coord_key = (elem.attrib["lat"], elem.attrib["lon"])
            if coord_key not in unique_nodes:
                unique_nodes[coord_key] = elem
            else:
                root.remove(elem)
        elif elem.tag == "way":
            node_refs = tuple(nd.attrib["ref"] for nd in elem.findall("nd"))
            if node_refs not in unique_ways:
                unique_ways[node_refs] = elem
            else:
                root.remove(elem)

    tree.write(output_file, encoding="UTF-8", xml_declaration=True)

def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    osm_files = glob.glob(os.path.join(script_dir, "*.osm"))

    cleaned_files = []
    for i, osm_file in enumerate(osm_files):
        cleaned_file = os.path.join(script_dir, f"cleaned_{i}.osm")
        clean_osm(osm_file, cleaned_file)
        cleaned_files.append(cleaned_file)

    output_file_with_duplicates = os.path.join(script_dir, "mapclean_with_duplicates.osm")
    merge_osm_files(cleaned_files, output_file_with_duplicates)

    # Remove temporary cleaned files
    for cleaned_file in cleaned_files:
        os.remove(cleaned_file)

    final_output_file = os.path.join(script_dir, "mapclean.osm")
    remove_duplicates(output_file_with_duplicates, final_output_file)

    # Remove the temporary file with duplicates
    os.remove(output_file_with_duplicates)

if __name__ == "__main__":
    main()



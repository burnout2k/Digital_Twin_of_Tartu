""" Places the street lights models into the correct position in the active Unreal scene """

import csv
import unreal

# Open CSV file
with open("/home/allan/carla/Unreal/CarlaUE4/Content/Carla/Maps/tartu_large/scripts/lights_unreal.csv") as file:
    reader = csv.DictReader(file)

    for row in reader:
        # Check if any of the required fields are missing or empty
        if row['X'] and row['Y'] and row['Z'] and row['Valgusti_suund']:
            x, y, z, angle = float(row['X']), -float(row['Y']), float(row['Z']), float(row['Valgusti_suund'])

            # Convert meters to centimeters (Unreal Engine uses centimeters)
            x *= 100
            y *= 100
            z *= 100        

            # Define location and rotation
            location = unreal.Vector(x, y, z)
            rotation = unreal.Rotator(0, 0, angle-90)

            # Load the asset
            asset_path = '/Game/Carla/Static/StreetLight/TartuLightSimple2.TartuLightSimple2'
            asset = unreal.load_asset(asset_path)

            # Create the asset in the world at the given location and rotation
            unreal.EditorLevelLibrary.spawn_actor_from_object(asset, location, rotation)
        else:
            # Optionally, log the skipped row or handle it differently
            print(f"Skipped row due to missing data: {row}")

print("DONE")


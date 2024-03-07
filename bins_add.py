""" Places the trash containers into the correct position in the active Unreal scene. Randomly chooses one of three available models for the bin """

import csv
import random
import unreal

# Paths for the three dumpster models
model_paths = [
    '/Game/Carla/Maps/tartu_large/benches/dumpster_Dumpster_Sm01Node.dumpster_Dumpster_Sm01Node',
    '/Game/Carla/Static/Dynamic/Trash/SM_Container.SM_Container',
    '/Game/Carla/Static/Dynamic/Trash/SM_Dumpster.SM_Dumpster'
]

# Open CSV file and read all rows
with open("/home/allan/carla/Unreal/CarlaUE4/Content/Carla/Maps/tartu_large/scripts/bins_unreal.csv") as file:
    reader = csv.DictReader(file)
    rows = list(reader)

# Randomize the order of rows
random.shuffle(rows)

# Process each row
for row in rows:
    x, y, z = float(row['X']), float(row['Y']), float(row['Z'])

    # Convert meters to centimeters (Unreal Engine uses centimeters)
    x *= 100
    y *= 100
    z *= 100        

    # Define location and rotation
    location = unreal.Vector(x, y, z)

    # Randomly select an asset path
    asset_path = random.choice(model_paths)
    asset = unreal.load_asset(asset_path)

    # Create the asset in the world at the given location
    unreal.EditorLevelLibrary.spawn_actor_from_object(asset, location)

print("DONE")


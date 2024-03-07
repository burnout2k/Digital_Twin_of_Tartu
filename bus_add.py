""" Places the bus stops models into the correct position in the active Unreal scene """


import csv
import unreal

# Open CSV file
with open("/home/allan/carla/Unreal/CarlaUE4/Content/Carla/Maps/tartu_large/scripts/bus_unreal.csv") as file:

    reader = csv.DictReader(file)

    for row in reader:
        x, y, z = float(row['X']), float(row['Y']), float(row['Z'])

        # Convert meters to centimeters (Unreal Engine uses centimeters)
        x *= 100
        y *= 100
        z *= 100        

	# Define location and rotation'/Game/Carla/Static/Dynamic/Trash/SM_Container.SM_Container'
        location = unreal.Vector(x, y, z)

        # Load the asset
        asset_path = '/Game/Carla/Maps/tartu_large/benches/busstop_busstop.busstop_busstop'
        asset = unreal.load_asset(asset_path)

        # Create the asset in the world at the given location and rotation
        unreal.EditorLevelLibrary.spawn_actor_from_object(asset, location)

print("DONE")

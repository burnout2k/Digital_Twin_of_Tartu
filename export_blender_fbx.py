""" Exports all blender scene objects as separate files in Filmbosx format  """
    
import bpy
import os

# specify path to directory where you want to export files
path_to_export = "C:/Users/burno/Downloads/maps/agisoft/ruudud/ala4b"

bpy.ops.object.select_all(action='DESELECT')

for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        obj.select_set(True)

        filepath = os.path.join(path_to_export, obj.name)
        
        # export to .fbx format
        bpy.ops.export_scene.fbx(filepath=filepath + ".fbx", use_selection=True)

        obj.select_set(False)
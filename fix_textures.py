""" Adjusts the brightness (makes it darker) and metallic, specular, roughness values of a material  """

import unreal

# Define the directory where the materials are located
content_directory = "/Game/Carla/Maps/tartu_large/agisoft/"

# List all assets in the content directory
all_assets = unreal.EditorAssetLibrary.list_assets(content_directory, recursive=False, include_folder=False)

# Filter for material assets that start with 'ala7' but not with 'ala7b'
material_assets = [asset for asset in all_assets if unreal.Paths.get_clean_filename(asset).startswith('ala4_2') and not unreal.Paths.get_clean_filename(asset).startswith('ala7b')]

# Loop through each filtered material asset
for material_path in material_assets:
    # Load the material asset
    material = unreal.EditorAssetLibrary.load_asset(material_path)
    
    # Verify it's a Material
    if isinstance(material, unreal.Material):
        # Start editing the material
        with unreal.ScopedEditorTransaction("Set Properties and Connect Texture Sample") as trans:
            material_editor_util = unreal.MaterialEditingLibrary
            
            # Construct the texture name and attempt to load it
            material_name = unreal.Paths.get_clean_filename(material_path).split('.')[0]
            texture_name = material_name + "_ncl1_1"
            texture_asset_path = "/Game" + content_directory.replace("/Game", "") + texture_name
            
            texture = unreal.EditorAssetLibrary.load_asset(texture_asset_path)
            if texture:
                # Create and configure the TextureSample node
                texture_sample_node = material_editor_util.create_material_expression(material, unreal.MaterialExpressionTextureSample, 0, 0)
                texture_sample_node.texture = texture
                
                # Create the Multiply node
                multiply_node = material_editor_util.create_material_expression(material, unreal.MaterialExpressionMultiply, 200, 0)
                
                # Create a Constant node for the Multiply input B
                constant_value_node = material_editor_util.create_material_expression(material, unreal.MaterialExpressionConstant, 200, -200)
                constant_value_node.r = 0.5
                
                # Connect the TextureSample node to the Multiply node input A
                material_editor_util.connect_material_expressions(texture_sample_node, 'RGB', multiply_node, 'A')
                
                # Connect the Constant node to the Multiply node input B
                material_editor_util.connect_material_expressions(constant_value_node, '', multiply_node, 'B')
                
                # Connect the Multiply node's output to the Base Color
                material_editor_util.connect_material_property(multiply_node, '', unreal.MaterialProperty.MP_BASE_COLOR)

            # Create and set constant nodes for Metallic, Specular, and Roughness
            # Set Metallic to 0
            metallic_constant_node = material_editor_util.create_material_expression(material, unreal.MaterialExpressionConstant, 200, -400)
            metallic_constant_node.r = 0.0
            material_editor_util.connect_material_property(metallic_constant_node, '', unreal.MaterialProperty.MP_METALLIC)
            
            # Set Specular to 0
            specular_constant_node = material_editor_util.create_material_expression(material, unreal.MaterialExpressionConstant, 200, -600)
            specular_constant_node.r = 0.0
            material_editor_util.connect_material_property(specular_constant_node, '', unreal.MaterialProperty.MP_SPECULAR)
            
            # Set Roughness to 0.9
            roughness_constant_node = material_editor_util.create_material_expression(material, unreal.MaterialExpressionConstant, 200, -800)
            roughness_constant_node.r = 0.9
            material_editor_util.connect_material_property(roughness_constant_node, '', unreal.MaterialProperty.MP_ROUGHNESS)

            # Save the changes to the material
            unreal.EditorAssetLibrary.save_loaded_asset(material)

print("Brightness adjustment for materials is complete.")


""" Filters trees in a way that no two trees are closer than 6 meters to each other  """

import pandas as pd
from sklearn.neighbors import KDTree

def remove_close_trees(tree_kdtree, min_distance, tree_coordinates):
    to_keep = set(range(len(tree_coordinates)))
    for i in range(len(tree_coordinates)):
        if i in to_keep:
            indices = tree_kdtree.query_radius([tree_coordinates[i]], r=min_distance)
            to_keep.difference_update(set(indices[0]) - {i})
    return to_keep

# Load the CSV file
file_path = 'trees.csv'  # Replace with your file path
trees_data = pd.read_csv(file_path)

# Assuming coordinates are already in meters
tree_coordinates_meters = list(zip(trees_data['X'], trees_data['Y']))

# Create KDTree for efficient distance calculations
tree_kdtree_meters = KDTree(tree_coordinates_meters)

# Remove trees to ensure a minimum distance of 6 meters between any two trees
min_distance_m = 6  # 6 meters
remaining_tree_indices = remove_close_trees(tree_kdtree_meters, min_distance_m, tree_coordinates_meters)

# Convert set to list for indexing
remaining_tree_indices_list = list(remaining_tree_indices)

# Filter the original DataFrame to keep only the remaining trees
remaining_trees_data = trees_data.loc[remaining_tree_indices_list]

# Save the filtered data to a new CSV file
remaining_trees_data.to_csv('filtered_trees_6m.csv', index=False)

print(f"Original number of trees: {len(tree_coordinates_meters)}")
print(f"Number of trees after filtering: {len(remaining_tree_indices_list)}")

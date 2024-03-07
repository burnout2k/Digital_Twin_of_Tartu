""" Shuffles the tree list around and splits them into deciduous and coniferous trees. After that, both groups are again divided into 3 subgroups and saved as CSV files """

import pandas as pd
import numpy as np

# Load the CSV file into a DataFrame
df = pd.read_csv('trees_unreal.csv')

df_leaf = df[df['type'] == 'Leht']
df_leaf_shuffled = df_leaf.sample(frac=1).reset_index(drop=True)
length = len(df_leaf_shuffled) // 3
df_leaf1 = df_leaf_shuffled[:length]
df_leaf2 = df_leaf_shuffled[length:2*length]
df_leaf3 = df_leaf_shuffled[2*length:]
df_leaf1.to_csv('df_leaf1.csv', index=False)
df_leaf2.to_csv('df_leaf2.csv', index=False)
df_leaf3.to_csv('df_leaf3.csv', index=False)

df_thorn = df[df['type'] == 'Okas']
df_thorn_shuffled = df_thorn.sample(frac=1).reset_index(drop=True)
length = len(df_thorn_shuffled) // 3
df_thorn1 = df_thorn_shuffled[:length]
df_thorn2 = df_thorn_shuffled[length:2*length]
df_thorn3 = df_thorn_shuffled[2*length:]
df_thorn1.to_csv('df_thorn1.csv', index=False)
df_thorn2.to_csv('df_thorn2.csv', index=False)
df_thorn3.to_csv('df_thorn3.csv', index=False)

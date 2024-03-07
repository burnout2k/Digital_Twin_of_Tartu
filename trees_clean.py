""" Adds altitude value to every tree as Z coordinate and renames and rearranges the columns dropping the unused data """

import pandas as pd
import numpy as np

# Load the CSV file into a DataFrame
df = pd.read_csv('trees.csv')

df['Z'] = np.nan

# List of column names to check
columns = ['54763_DTM_1m', '54761_DTM_1m', '54754_DTM_1m', '54752_DTM_1m', '54663_DTM_1m', '54654_DTM_1m']

# Copy over the value from the specified columns to the new column 'Z'
for column in columns:
    # Check if column has any non-NaN values
    if df[column].count() > 0:
        # Copy non-NaN values to column 'Z'
        df.loc[df[column].notna(), 'Z'] = df.loc[df[column].notna(), column]

df = df[['fid', 'X', 'Y', 'Z','z','MBG_Diameter','tree_type']]

rename_dict = {
    'z': 'height',
    'MBG_Diameter': 'diameter',
    'tree_type': 'type'
}

df = df.rename(columns=rename_dict)

df.to_csv('trees_clean.csv', index=False)

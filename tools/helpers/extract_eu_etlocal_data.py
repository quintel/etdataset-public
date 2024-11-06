'''
This script obtains ETLocal key values for the EU datasets through the api.
The result is a csv files containing the EU countries and all ETLocal keys and values.
'''

import requests
import pandas as pd

# List of GEO_IDs
geo_ids = ['AT','BE','BG','CY','CZ','DE','DK','EE','ES','FI','FR','EL','HR','HU','IE','IT','LT','LU','LV','MT','NL','PL','PT','RO','SE','SI','SK','EU27','UK']  # Replace these with your actual GEO_IDs

# URL of the API endpoint
base_url = 'https://data.energytransitionmodel.com/api/v1/exports/'

# Function to fetch data for a single GEO_ID
def fetch_data(geo_id):
    url = base_url + geo_id
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for {geo_id}")
        return None

# Fetch data for each GEO_ID and store in a list
data_list = [fetch_data(geo_id) for geo_id in geo_ids]

# Convert data to DataFrame
dfs = []
for i, data in enumerate(data_list):
    if data is not None:
        df = pd.DataFrame(data)
        # Add a column for GEO_ID for reference
        df['GEO_ID'] = geo_ids[i]
        # Reorder columns to put GEO_ID as the first column
        cols = df.columns.tolist()
        cols = ['GEO_ID'] + [col for col in cols if col != 'GEO_ID']
        df = df[cols]
        dfs.append(df)

# Concatenate DataFrames
final_df = pd.concat(dfs, ignore_index=True)

# Export to CSV
final_df.to_csv('exported_data.csv', index=False)

print("Data exported successfully to 'extracted_eu_etlocal_data.csv'.")

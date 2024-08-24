import pandas as pd
import glob
import os
import time

# Define the paths
input_folder = 'Scrapped'
output_folder = 'Clean Data'

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Path to CSV files in the input folder
path = os.path.join(input_folder, "*.csv")

# Get all CSV files in the folder
all_files = glob.glob(path)

# Create a list to hold the dataframes
dataframes = []

# Columns to exclude
exclude_columns = ['Introduction', 'Store Shopping', 'In Store Pickup', 'In Store Pickup']

# Track progress
total_files = len(all_files)
print(f'Total files found: {total_files}')

# Read, process, and filter CSV files
for i, filename in enumerate(all_files, start=1):
    print(f'Reading file {i}/{total_files}: {filename}')
    df = pd.read_csv(filename)
    
    # Drop the columns that should be excluded
    df = df.drop(columns=[col for col in exclude_columns if col in df.columns])
    
    # Drop rows where 'Phone Number' is empty
    if 'Phone Number' in df.columns:
        df = df.dropna(subset=['Phone Number'])
        
        # Remove spaces from the 'Phone Number' column
        df['Phone Number'] = df['Phone Number'].astype(str).str.replace(' ', '', regex=False)
    
    dataframes.append(df)

# Concatenate all dataframes into a single dataframe
merged_df = pd.concat(dataframes, ignore_index=True)

# Find and remove duplicate rows
initial_row_count = len(merged_df)
merged_df = merged_df.drop_duplicates()
final_row_count = len(merged_df)
duplicates_deleted = initial_row_count - final_row_count

# Print out the number of duplicates deleted
print(f'Total rows before removing duplicates: {initial_row_count}')
print(f'Total rows after removing duplicates: {final_row_count}')
print(f'Number of duplicate rows deleted: {duplicates_deleted}')

# Define the path for the output CSV file
output_file = os.path.join(output_folder, 'merged_file.csv')

# Save the merged dataframe to a new CSV file
merged_df.to_csv(output_file, index=False)

print(f'Merged file saved to {output_file}')

# Timer
print('Waiting for 15 seconds...')
time.sleep(15)

print('Done!')

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

# Track the original number of rows
original_row_count = len(merged_df)

# Identify duplicates and drop only one instance per duplicate
duplicates = merged_df[merged_df.duplicated(subset=['Phone Number'], keep=False)]
duplicates_removed = 0

# Iterate over duplicate phone numbers and keep only one instance
for phone_number in duplicates['Phone Number'].unique():
    duplicate_rows = merged_df[merged_df['Phone Number'] == phone_number]
    if len(duplicate_rows) > 1:
        duplicates_removed += len(duplicate_rows) - 1
        # Keep only the first occurrence and drop the rest
        merged_df = merged_df[~(merged_df['Phone Number'] == phone_number) | (merged_df.index == duplicate_rows.index[0])]

# Get the total number of rows after deduplication
final_row_count = len(merged_df)

print(f'Total rows before deduplication: {original_row_count}')
print(f'Total rows after deduplication: {final_row_count}')
print(f'Duplicates removed: {duplicates_removed}')

# Define the path for the output CSV file
output_file = os.path.join(output_folder, 'merged_file.csv')

# Save the merged dataframe to a new CSV file
merged_df.to_csv(output_file, index=False)

print(f'Merged file saved to {output_file}')

# Timer
print('Waiting for 15 seconds...')
time.sleep(15)

print('Done!')

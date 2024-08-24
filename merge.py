import pandas as pd
import os
import time

# Define the paths
input_folder = 'Scrapped'
output_folder = 'Clean Data'

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# List all CSV files in the input folder
csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

# Initialize an empty list to store DataFrames
dfs = []

# Track the number of files processed
total_files = len(csv_files)

# Read and append each CSV file into the list
for i, csv_file in enumerate(csv_files, start=1):
    file_path = os.path.join(input_folder, csv_file)
    df = pd.read_csv(file_path)
    dfs.append(df)
    print(f"Processed file {i} of {total_files}: {csv_file}")

# Concatenate all DataFrames into one
merged_df = pd.concat(dfs, ignore_index=True)

# Count the number of empty phone numbers before removing them
empty_phone_numbers_count = merged_df['Phone Number'].isna().sum() + (merged_df['Phone Number'] == '').sum()
print(f"Number of empty phone numbers found: {empty_phone_numbers_count}")

# Remove rows with empty 'Phone Number'
merged_df = merged_df[merged_df['Phone Number'].notna() & (merged_df['Phone Number'] != '')]

# Remove spaces from 'Phone Number'
merged_df['Phone Number'] = merged_df['Phone Number'].astype(str).str.replace(' ', '', regex=False)

# Remove leading zeros from 'Phone Number'
merged_df['Phone Number'] = merged_df['Phone Number'].str.lstrip('0')

# Ensure 'Phone Number' is 10 digits long
merged_df['Phone Number'] = merged_df['Phone Number'].str.zfill(10)

# Number of rows before removing duplicates
total_rows_before = len(merged_df)

# Remove duplicates based on 'Phone Number', keeping the first occurrence
cleaned_df = merged_df.drop_duplicates(subset='Phone Number', keep='first')

# Number of rows after removing duplicates
total_rows_after = len(cleaned_df)

# Calculate the number of duplicates removed
duplicates_removed = total_rows_before - total_rows_after

# Define the output file path
output_file = os.path.join(output_folder, 'cleaned_data.csv')

# Save the cleaned DataFrame to a new CSV file
cleaned_df.to_csv(output_file, index=False)

print(f"Data cleaned and saved to {output_file}")
print(f"Total files processed: {total_files}")
print(f"Total rows before removing duplicates: {total_rows_before}")
print(f"Total rows after removing duplicates: {total_rows_after}")
print(f"Duplicates removed: {duplicates_removed}")

# Wait for 5 seconds before exiting
print("Exiting in 15 seconds...")
time.sleep(15)

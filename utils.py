import os
import sys
import pandas as pd
import data

async def get_search_list():
    try:
        choice = input("Would you like to input search term manually (1) or use input.txt (2)? ")
        if choice == '1':
            search_for = input("Please enter your search term: ")
            return [search_for.strip()]
        elif choice == '2':
            input_file_name = 'input.txt'
            input_file_path = os.path.join(os.getcwd(), input_file_name)
            if os.path.exists(input_file_path):
                with open(input_file_path, 'r') as file:
                    return [line.strip() for line in file.readlines()]
            else:
                print(f'Error: {input_file_name} not found.')
                sys.exit()
        else:
            print('Invalid choice. Exiting.')
            sys.exit()
    except Exception as e:
        print(f"An error occurred while getting the search list: {e}")
        sys.exit()

def save_data(search_for):
    try:
        # Ensure all lists in data.data are of the same length
        min_length = min(len(data.data[key]) for key in data.data.keys())
        for key in data.data.keys():
            if len(data.data[key]) > min_length:
                data.data[key] = data.data[key][:min_length]

        map_data = {
            'Name': data.data['names'], 'Address': data.data['addresses'], 'Phone': data.data['phones'],
            'Website': data.data['websites'], 'Google Link': data.data['links'],
            'Latitude': data.data['latitudes'], 'Longitude': data.data['longitudes'],
            'Reviews_Count': data.data['reviews_count'], 'Average Rates': data.data['rates']
        }
        df = pd.DataFrame(map_data)
        print(df)
        output_folder = 'output'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        filename = search_for.replace(' ', '_').lower()
        df.to_excel(os.path.join(output_folder, f'{filename}.xlsx'), index=False)
    except Exception as e:
        print(f"An error occurred while saving data: {e}")


def merge_excel_files():
    try:
        output_folder = 'output'
        all_files = [os.path.join(output_folder, f) for f in os.listdir(output_folder) if f.endswith('.xlsx')]
        combined_df = pd.concat([pd.read_excel(f) for f in all_files])
        combined_df.drop_duplicates(subset=['Google Link'], inplace=True)
        combined_df.to_excel(os.path.join(output_folder, 'merged_output.xlsx'), index=False)
        print("Merged file saved as 'merged_output.xlsx'.")
    except Exception as e:
        print(f"An error occurred while merging Excel files: {e}")

def parse_coordinates():
    try:
        for coordinate in data.data['links']:
            try:
                # Split the link by '@' and take the part after the last '@'
                parts = coordinate.split('@')[-1].split(',')
                data.data['latitudes'].append(parts[0])
                data.data['longitudes'].append(parts[1])
            except IndexError:
                data.data['latitudes'].append(None)
                data.data['longitudes'].append(None)
    except Exception as e:
        print(f"An error occurred while parsing coordinates: {e}")

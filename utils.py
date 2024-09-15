import os
import sys
import pandas as pd
import data
from openpyxl import load_workbook

async def get_search_list():
    try:
        choice = input("Would you like to input search term manually (1) or use Query.txt (2)? ")
        if choice == '1':
            search_for = input("Please enter your search term: ")
            return [search_for.strip()]
        elif choice == '2':
            input_file_name = 'Query.txt'
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
            'Names': data.data['names'], 'Address': data.data['addresses'],'Plus Code': data.data['plus_code'], 'Phone Number': data.data['phones'],
            'Website': data.data['websites'], 'Google Link': data.data['links'],
            'Latitude': data.data['latitudes'], 'Longitude': data.data['longitudes'],
            'Reviews_Count': data.data['reviews_count'], 'Average Rates': data.data['rates'], 'Type': data.data['type']
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
        
        output_file = os.path.join(output_folder, 'merged_output.xlsx')
        combined_df.to_excel(output_file, index=False)
        print("Merged file saved as 'merged_output.xlsx'.")
        
        # Adjust column widths
        adjust_column_width(output_file)
        
    except Exception as e:
        print(f"An error occurred while merging Excel files: {e}")

def adjust_column_width(file_path):
    try:
        # Load the workbook and the sheet
        workbook = load_workbook(file_path)
        worksheet = workbook.active
        
        # Iterate over all columns and set the column width based on the maximum length of content
        for col in worksheet.columns:
            max_length = 0
            col_letter = col[0].column_letter  # Get the column letter (A, B, C, etc.)
            
            for cell in col:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass
            
            adjusted_width = max_length + 2  # Add some padding
            worksheet.column_dimensions[col_letter].width = adjusted_width
        
        # Save the workbook after adjusting column widths
        workbook.save(file_path)
        print("Column widths adjusted for better viewing.")
        
    except Exception as e:
        print(f"An error occurred while adjusting column widths: {e}")

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

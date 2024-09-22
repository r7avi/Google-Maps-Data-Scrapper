import os
import sys
import pandas as pd
import data
from openpyxl import load_workbook
import paramiko

# SSH and SFTP credentials
ssh_host = 'YOUR_SERVER_SSH_IP'
ssh_port = 22
ssh_user = 'USERNAME' # Please use root
ssh_password = 'YOUR_SSH_PASSWORD'

async def get_search_list():
    try:
        # Directly use Query.txt without asking for user input
        input_file_name = 'Query.txt'
        input_file_path = os.path.join(os.getcwd(), input_file_name)
        if os.path.exists(input_file_path):
            with open(input_file_path, 'r') as file:
                return [line.strip() for line in file.readlines()]
        else:
            print(f'Error: {input_file_name} not found.')
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
            'Names': data.data['names'], 'Address': data.data['addresses'], 'Plus Code': data.data['plus_code'], 'Phone Number': data.data['phones'],
            'Website': data.data['websites'], 'Google Link': data.data['links'],
            'Latitude': data.data['latitudes'], 'Longitude': data.data['longitudes'],
            'Reviews_Count': data.data['reviews_count'], 'Average Rates': data.data['rates'], 'Type': data.data['type']
        }
        df = pd.DataFrame(map_data)
        output_folder = 'output'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        filename = search_for.replace(' ', '_').lower()
        file_path = os.path.join(output_folder, f'{filename}.xlsx')
        df.to_excel(file_path, index=False)

        # Upload the file to the cloud
        upload_to_cloud(file_path)

        # Remove the processed line from Query.txt
        update_query_file(search_for)

    except Exception as e:
        print(f"An error occurred while saving data: {e}")

def update_query_file(search_for):
    try:
        input_file_name = 'Query.txt'
        input_file_path = os.path.join(os.getcwd(), input_file_name)
        if os.path.exists(input_file_path):
            with open(input_file_path, 'r') as file:
                lines = file.readlines()
            # Remove the processed search term
            lines = [line for line in lines if line.strip() != search_for]
            with open(input_file_path, 'w') as file:
                file.writelines(lines)

            # Upload the updated Query.txt to the cloud
            upload_to_cloud(input_file_path)

        else:
            print(f'Error: {input_file_name} not found.')
    except Exception as e:
        print(f"An error occurred while updating the query file: {e}")

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

        # Upload the merged file to the cloud
        upload_to_cloud(output_file)
        
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

def upload_to_cloud(local_file_path):
    try:
        # Create an SSH client
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the remote server
        ssh_client.connect(ssh_host, port=ssh_port, username=ssh_user, password=ssh_password)

        # Create an SFTP session
        sftp = ssh_client.open_sftp()

        # Define the remote path where the file will be uploaded
        remote_file_path = f'/home/data/v2/{os.path.basename(local_file_path)}'
        remote_dir = os.path.dirname(remote_file_path)

        # Ensure the remote directory exists
        ssh_client.exec_command(f"mkdir -p {remote_dir}")

        # Upload the file to the remote server
        sftp.put(local_file_path, remote_file_path)
        print(f'File uploaded to {remote_file_path}.')

        # Close the SFTP session and SSH connection
        sftp.close()
        ssh_client.close()
    except Exception as e:
        print(f"An error occurred while uploading the file to the cloud: {e}")


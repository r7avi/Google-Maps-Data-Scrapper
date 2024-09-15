import pandas as pd
import re
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to validate email addresses
def is_valid_email(email):
    # Simple regex pattern for basic email validation
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

# Function to select a file and validate emails
def validate_emails():
    # Create a Tkinter root window (it will be hidden)
    root = tk.Tk()
    root.withdraw()
    
    # Open file dialog to select the file (CSV or Excel)
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx;*.xls")]
    )
    
    if not file_path:
        messagebox.showinfo("No file selected", "No file was selected. Exiting.")
        return
    
    try:
        # Determine file type and read the file into a DataFrame
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Please select a CSV or Excel file.")

        # Check if 'Email' column exists
        if 'Email' not in df.columns:
            messagebox.showerror("Column Not Found", "No 'Email' column found in the selected file.")
            return

        # Validate emails
        df['Valid'] = df['Email'].apply(is_valid_email)
        
        # Open file dialog to save the results (CSV or Excel)
        output_file = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")],
            title="Save validated emails as"
        )
        
        if not output_file:
            messagebox.showinfo("No output file", "No output file specified. Exiting.")
            return
        
        # Save results to the selected file format
        if output_file.endswith('.csv'):
            df.to_csv(output_file, index=False)
        elif output_file.endswith(('.xlsx', '.xls')):
            df.to_excel(output_file, index=False)
        else:
            raise ValueError("Unsupported file format for saving. Please select an Excel or CSV file.")

        messagebox.showinfo("Success", f"Validated emails saved to {output_file}")
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        print(f"An error occurred: {e}")

# Run the function
validate_emails()

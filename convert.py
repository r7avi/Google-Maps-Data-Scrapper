import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import os

def process_file(input_file_path, output_file_path, front_word, back_word):
    # Open the input file and read lines
    with open(input_file_path, 'r') as infile:
        lines = infile.readlines()
    
    # Process lines and add text
    processed_lines = [f'{front_word} {line.strip()}{back_word}\n' for line in lines]
    
    # Write the processed lines to the output file
    with open(output_file_path, 'w') as outfile:
        outfile.writelines(processed_lines)
    
    print(f'File saved as {output_file_path}')

def main():
    # Create a Tkinter root window (it will not be shown)
    root = tk.Tk()
    root.withdraw()
    
    # Open file dialog to select the input file
    input_file_path = filedialog.askopenfilename(
        title="Select your .txt file",
        filetypes=[("Text files", "*.txt")]
    )
    
    if not input_file_path:
        print("No file selected. Exiting.")
        return
    
    # Prompt for front and back words
    front_word = simpledialog.askstring("Input", "Enter the text to add in front:")
    back_word = simpledialog.askstring("Input", "Enter the text to add at the end:")
    
    if front_word is None or back_word is None:
        print("No input provided. Exiting.")
        return
    
    # Generate the output file path
    base, ext = os.path.splitext(input_file_path)
    output_file_path = f"{base}_converted{ext}"
    
    # Process the file
    process_file(input_file_path, output_file_path, front_word, back_word)

if __name__ == "__main__":
    main()

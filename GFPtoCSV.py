import xml.etree.ElementTree as ET
import csv
import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

def extract_line_data_with_positions(line_element):
    result = {}
    # Get 'name' attribute from <Line>
    result['name'] = line_element.attrib.get('name', '')

    # Find the DataFile element
    data_file = line_element.find('DataFile')
    if data_file is not None:
        positions = data_file.findall('Position')
        # Get first and second Position elements, if available
        if len(positions) > 0:
            for key, val in positions[0].attrib.items():
                if key not in ['normalized_file_pos', 'units', 'Z']:
                    result[f'Position1_{key}'] = val
        if len(positions) > 1:
            for key, val in positions[1].attrib.items():
                if key not in ['normalized_file_pos', 'units', 'Z']:
                    result[f'Position2_{key}'] = val

    return result

def convert_gfp_to_csv(input_path, output_path):
    tree = ET.parse(input_path)
    root = tree.getroot()

    # Find the <LineSet> element and extract data from its <Line> children
    line_set = root.find('.//LineSet')
    if line_set is None:
        raise ValueError("No <LineSet> element found in the file.")

    data = []
    all_fieldnames = set()
    for line in line_set.findall('Line'):
        line_data = extract_line_data_with_positions(line)
        data.append(line_data)
        all_fieldnames.update(line_data.keys())

    # Ensure 'name' is the first column
    all_fieldnames.discard('name')
    fieldnames = ['name'] + sorted(all_fieldnames)

    with open(output_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow({key: row.get(key, '') for key in fieldnames})

    messagebox.showinfo("Success", f"CSV file successfully created at: {output_path}")

def main():
    root = tk.Tk()
    root.withdraw()

    input_path = filedialog.askopenfilename(
        title="Select GFP file",
        filetypes=[("GFP files", "*.gfp")]
    )
    if not input_path:
        messagebox.showerror("Error", "No input file selected.")
        return

    output_name = simpledialog.askstring("Output CSV", "Enter output CSV file name (without extension):")
    if not output_name:
        messagebox.showerror("Error", "No output file name provided.")
        return

    output_path = os.path.join(os.path.dirname(input_path), output_name + '.csv')

    try:
        convert_gfp_to_csv(input_path, output_path)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

if __name__ == "__main__":
    main()

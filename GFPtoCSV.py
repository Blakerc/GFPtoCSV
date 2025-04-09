import xml.etree.ElementTree as ET
import csv
import os
import tkinter as tk
from tkinter import filedialog, messagebox

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


def browse_file(entry):
    path = filedialog.askopenfilename(filetypes=[("GFP files", "*.gfp")])
    if path:
        entry.delete(0, tk.END)
        entry.insert(0, path)


def main():
    root = tk.Tk()
    root.title("GFP to CSV Converter")
    
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width)
    y = (root.winfo_screenheight() // 2) - (height)
    root.geometry(f'+{x}+{y}')

    tk.Label(root, text="GFP File:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
    entry_path = tk.Entry(root, width=50)
    entry_path.grid(row=0, column=1, padx=5, pady=5)
    tk.Button(root, text="Browse", command=lambda: browse_file(entry_path)).grid(row=0, column=2, padx=5, pady=5)

    tk.Label(root, text="Output CSV:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
    entry_name = tk.Entry(root, width=50)
    entry_name.grid(row=1, column=1, padx=5, pady=5)

    def on_submit():
        input_path = entry_path.get().strip()
        output_name = entry_name.get().strip()

        if not input_path or not os.path.isfile(input_path):
            messagebox.showerror("Error", "Please provide a valid GFP file path.")
            return
        if not output_name:
            messagebox.showerror("Error", "Please enter a name for the output CSV file.")
            return

        output_path = os.path.join(os.path.dirname(input_path), output_name + '.csv')
        
        if os.path.exists(output_path):
            messagebox.showerror("Error", f"A file named '{output_name}.csv' already exists in this directory.")
            return

        try:
            convert_gfp_to_csv(input_path, output_path)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")

    convert_button = tk.Button(root, text="Convert", command=on_submit)
    convert_button.grid(row=2, column=0, columnspan=3, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()

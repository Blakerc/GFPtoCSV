import csv
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def convert_gfp_to_csv(gfp_file, csv_file, delimiter):
    """Convert GFP file to CSV."""
    try:
        with open(gfp_file, "r") as gfp:
            lines = gfp.readlines()

        if not lines:
            messagebox.showwarning("Warning", "The .gfp file is empty.")
            return

        # Extract headers using the specified delimiter
        headers = lines[0].strip().split(delimiter)

        # Write to CSV
        with open(csv_file, "w", newline="") as csv_out:
            writer = csv.writer(csv_out)
            writer.writerow(headers)  # Write headers

            # Write data rows
            for line in lines[1:]:
                row = line.strip().split(delimiter)
                writer.writerow(row)

        messagebox.showinfo("Success", f"Conversion complete: {csv_file}")

    except FileNotFoundError:
        messagebox.showerror("Error", f"The file '{gfp_file}' was not found.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def select_gfp_file():
    """Open file dialog to select the .gfp file starting in the script's directory."""
    initial_dir = os.path.dirname(os.path.abspath(__file__))
    gfp_path = filedialog.askopenfilename(initialdir=initial_dir, filetypes=[("GFP files", "*.gfp")])
    
    if gfp_path:
        gfp_entry.delete(0, tk.END)
        gfp_entry.insert(0, gfp_path)

def select_csv_file():
    """Open file dialog to select the output .csv file starting in the script's directory."""
    initial_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = filedialog.asksaveasfilename(initialdir=initial_dir, defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    
    if csv_path:
        csv_entry.delete(0, tk.END)
        csv_entry.insert(0, csv_path)

def start_conversion():
    """Start the conversion process."""
    gfp_file = gfp_entry.get().strip()
    csv_file = csv_entry.get().strip()
    delimiter = delimiter_entry.get().strip()

    if not gfp_file or not csv_file:
        messagebox.showwarning("Warning", "Please select both GFP and CSV files.")
        return

    # Handle special characters like tab
    if delimiter.lower() == "\\t":
        delimiter = "\t"

    convert_gfp_to_csv(gfp_file, csv_file, delimiter)

# GUI
root = tk.Tk()
root.title("GFP to CSV Converter")
root.geometry("500x300")
root.resizable(False, False)

# Labels, entries, convert button
tk.Label(root, text="Select .gfp file:").pack(pady=(10, 0))
gfp_entry = tk.Entry(root, width=50)
gfp_entry.pack(pady=5)
tk.Button(root, text="Browse", command=select_gfp_file).pack()

tk.Label(root, text="Select output .csv file:").pack(pady=(10, 0))
csv_entry = tk.Entry(root, width=50)
csv_entry.pack(pady=5)
tk.Button(root, text="Browse", command=select_csv_file).pack()

tk.Label(root, text="Enter delimiter (optional):").pack(pady=(10, 0))
delimiter_entry = tk.Entry(root, width=10)
delimiter_entry.pack(pady=5)
delimiter_entry.insert(0, "|")  # Default delimiter

tk.Button(root, text="Convert", command=start_conversion, bg="green", fg="white").pack(pady=20)

root.mainloop()

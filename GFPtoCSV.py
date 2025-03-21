import csv
import os

def convert_gfp_to_csv(gfp_file, csv_file, delimiter):
    try:
        # Get the script's directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Create full paths
        gfp_path = os.path.join(script_dir, gfp_file)
        csv_path = os.path.join(script_dir, csv_file)

        with open(gfp_path, "r") as gfp:
            lines = gfp.readlines()

        if not lines:
            print("The .gfp file is empty.")
            return

        # Extract headers using the specified delimiter
        headers = lines[0].strip().split(delimiter)

        # Write to CSV
        with open(csv_path, "w", newline="") as csv_out:
            writer = csv.writer(csv_out)
            writer.writerow(headers)  # Write headers

            # Write data rows
            for line in lines[1:]:
                row = line.strip().split(delimiter)
                writer.writerow(row)

        print(f"Conversion complete: {csv_path}")

    except FileNotFoundError:
        print(f"Error: The file '{gfp_file}' was not found in the script directory.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Get list of .gfp files in the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
gfp_files = [f for f in os.listdir(script_dir) if f.endswith(".gfp")]

# Display available .gfp files
print("\nAvailable .gfp files in the script directory:")
for idx, file in enumerate(gfp_files, start=1):
    print(f"{idx}. {file}")

# Prompt for filenames and delimiter
gfp_file = input("\nEnter the .gfp filename (including extension): ").strip()
csv_file = input("Enter the output .csv filename: ").strip()
delimiter = input("Enter the delimiter used in the .gfp file (e.g., ',', '\\t', '|', ' '): ").strip()

# Handle special characters like tab
if delimiter.lower() == "\\t":
    delimiter = "\t"

# Run the conversion
convert_gfp_to_csv(gfp_file, csv_file, delimiter)
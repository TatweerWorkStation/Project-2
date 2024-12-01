import os
import csv
import re

# Base directory for reports
base_dir = os.path.join(os.getcwd(), "Reports")

# CSV file path
csv_file_path = os.path.join(os.getcwd(), "reports.csv")

# Function to extract the year from a file name
def extract_year(file_name):
    # Find all 4-digit sequences
    years = re.findall(r'(?<!\d)(\d{4})(?!\d)', file_name)
    
    # Convert to integers and filter valid years
    valid_years = [int(year) for year in years if 1900 <= int(year) <= 2100]
    
    # Return the latest year if available
    return str(max(valid_years)) if valid_years else 'عام'

# Get all folder names in the base directory
folders = [folder for folder in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, folder))]

# Open the CSV file for writing
with open(csv_file_path, "w", newline="", encoding="utf-8") as csv_file:
    fieldnames = ["id", "report_type", "year", "name", "pdf_path", "md_path"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    # Process each folder
    row_id = 1
    for folder in folders:
        report_type = folder
        folder_path = os.path.join(base_dir, folder)

        # Check if the folder exists
        if os.path.exists(folder_path):
            # Group files by base name (ignoring extensions)
            file_groups = {}
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)

                if os.path.isfile(file_path):
                    base_name, ext = os.path.splitext(file_name)
                    print(ext)
                    if base_name not in file_groups:
                        file_groups[base_name] = {}
                    file_groups[base_name][ext] = file_path

            # Write records to the CSV file
            for base_name, files in file_groups.items():
                pdf_file_path = files.get(".pdf")
                md_file_path = files.get(".md")

                # Extract the year from the file name
                year = extract_year(base_name)

                # Write to the CSV file
                writer.writerow({
                    "id": row_id,
                    "report_type": report_type,
                    "year": year,
                    "name": base_name,
                    "pdf_path": pdf_file_path,
                    "md_path": md_file_path
                })
                row_id += 1

print("CSV file created and populated with PDF and MD file paths.")
import sqlite3
import os
import re

# Base directory for reports
base_dir = os.path.join(os.getcwd(), "Reports")

# Database path
db_path = os.path.join(os.getcwd(), "Database", "reports.db")


# Folder names representing report types
folders = [
    # "إحصاءات التجارة الخارجية",
    # "احصائيات الناتج المحلي الإجمالي",
    # "احصائيات نقدية ومصرفية",
    # "إستخدامات المصارف للنقد الأجنبي",
    # "الدفع الإلكتروني",
    # "الرقم القياسي لنفقة المعيشة",
    # "النشرة الاقتصادية",
    # "أوراق التعاون الدولي",
    # "تقارير رقابية",
    # "ميزان المدفوعات",
    # "بيانات الإيراد والإنفاق",
    # "تقارير سنوية",
    # "عمليات السوق",
    # "أداء المصارف الليبية",
]

# Function to extract the year from a file name
def extract_year(file_name):
    # Find all 4-digit sequences
    years = re.findall(r'(?<!\d)(\d{4})(?!\d)', file_name)
    
    # Convert to integers and filter valid years
    valid_years = [int(year) for year in years if 1900 <= int(year) <= 2100]
    
    # Return the latest year if available
    return str(max(valid_years)) if valid_years else 'عام'

# Connect to the database
with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()

    # Create the reports table with columns for both PDF and MD files
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_type TEXT NOT NULL,
        year TEXT,
        path TEXT NOT NULL,
        name TEXT NOT NULL,
        pdf_file BLOB,
        md_file BLOB,
        UNIQUE(report_type, name) ON CONFLICT REPLACE
    )
    """)

    # Process each folder
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
                    if base_name not in file_groups:
                        file_groups[base_name] = {}
                    file_groups[base_name][ext] = file_path

            # Insert or update records in the database
            for base_name, files in file_groups.items():
                pdf_file_data = None
                md_file_data = None

                # Read the PDF file content, if available
                if '.pdf' in files:
                    try:
                        with open(files['.pdf'], "rb") as pdf_file:
                            pdf_file_data = pdf_file.read()
                    except Exception as e:
                        print(f"Error reading PDF file {files['.pdf']}: {e}")

                # Read the MD file content, if available
                if '.md' in files:
                    try:
                        with open(files['.md'], "rb") as md_file:
                            md_file_data = md_file.read()
                    except Exception as e:
                        print(f"Error reading MD file {files['.md']}: {e}")

                # Extract the year from the file name
                year = extract_year(base_name)

                # Insert into the database
                try:
                    cursor.execute("""
                    INSERT INTO reports (report_type, year, path, name, pdf_file, md_file)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """, (report_type, year, folder_path, base_name, pdf_file_data, md_file_data))
                except Exception as e:
                    print(f"Error inserting data for {base_name}: {e}")

    # Commit the changes to the database
    conn.commit()

print("Database recreated and populated with PDF and MD files.")

# Example query: Retrieve records where both PDF and MD files are present
with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("""
    SELECT report_type, year, name, LENGTH(pdf_file), LENGTH(md_file)
    FROM reports
    WHERE pdf_file IS NOT NULL AND md_file IS NOT NULL
    """)
    results = cursor.fetchall()

    for row in results:
        print(row)
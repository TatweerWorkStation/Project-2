import sqlite3
import os
import re

# Base directory relative to the script's location
base_dir = os.path.join(os.path.dirname(__file__), "Project-2")
db_path = os.path.join(base_dir, "Database", "reports.db")
reports_dir = os.path.join(base_dir, "Reports")

# Ensure the parent directory for the database exists
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Folders inside the "Reports" directory
folders = [
    "إحصاءات التجارة الخارجية",
    "إحصائيات الناتج المحلي الإجمالي",
    "إحصائيات نقدية ومصرفية",
    "إستخدامات المصارف للنقد الأجنبي",
    "الدفع الإلكتروني",
    "الرقم القياسي لنفقة المعيشة",
    "النشرة الإقتصادية",
    "أوراق التعاون الدولي",
    "تقارير سنوية",
    "ميزان المدفوعات"
]

# Function to extract a year from the filename
def extract_year(file_name):
    match = re.search(r'(?<!\d)(\d{4})(?!\d)', file_name)
    if match:
        year = int(match.group(1))
        if 1900 <= year <= 2100:
            return str(year)
    return 'NA'

try:
    # Connect to the SQLite database (creates the file if not present)
    with sqlite3.connect(db_path) as conn:
        print(f"Connected to database: {db_path}")
        cursor = conn.cursor()

        # Create the table if it doesn't already exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_type TEXT NOT NULL,
            year TEXT,
            path TEXT NOT NULL,
            name TEXT NOT NULL,
            file BLOB NOT NULL,
            UNIQUE(report_type, name) ON CONFLICT REPLACE 
        )
        """)

        # Iterate through folders and files
        for folder in folders:
            report_type = folder
            folder_path = os.path.join(reports_dir, folder)

            if os.path.exists(folder_path):
                for file_name in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, file_name)

                    if os.path.isfile(file_path):
                        try:
                            with open(file_path, "rb") as file:
                                file_data = file.read()

                            year = extract_year(file_name)

                            cursor.execute("""
                            INSERT INTO reports (report_type, year, path, name, file)
                            VALUES (?, ?, ?, ?, ?)
                            """, (report_type, year, file_path, file_name, file_data))

                        except Exception as e:
                            print(f"Error processing file {file_path}: {e}")

        conn.commit()
        print("Database created and populated successfully.")

except sqlite3.Error as e:
    print(f"SQLite error: {e}")
except Exception as e:
    print(f"General error: {e}")

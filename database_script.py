import sqlite3
import os

# Database file
db_path = r"C:\Users\A.I\Documents\Tatweer\Project 2\Database\reports.db"

# Directory structure
base_dir = r"C:\Users\A.I\Documents\Tatweer\Project 2\Reports"
folders = ["احصائيات نقدية ومصرفية", "النشرة الإقتصادية", "تقارير سنوية"]

# Create the database and table
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create the schema
cursor.execute("""
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_type TEXT NOT NULL,
    year INTEGER NOT NULL,
    path TEXT NOT NULL,
    name TEXT NOT NULL,
    file BLOB NOT NULL
)
""")
conn.commit()

# Helper function to get year from file name (assuming year is part of the name)
def extract_year(file_name):
    for word in file_name.split():
        if word.isdigit() and len(word) == 4:
            return int(word)
    return None

# Insert files into the database
for folder in folders:
    report_type = folder
    folder_path = os.path.join(base_dir, folder)

    if os.path.exists(folder_path):
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)

            if os.path.isfile(file_path):
                with open(file_path, "rb") as file:
                    file_data = file.read()

                year = extract_year(file_name) or 0  # Default to 0 if year not found
                cursor.execute("""
                INSERT INTO reports (report_type, year, path, name, file)
                VALUES (?, ?, ?, ?, ?)
                """, (report_type, year, file_path, file_name, file_data))

conn.commit()
conn.close()

print("Database created and populated successfully!")

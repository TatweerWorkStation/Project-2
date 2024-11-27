import sqlite3
import os
import re

# Database file (use absolute path if needed)
db_path = r"C:\Users\A.I\Documents\Tatweer\Project 2\Database\reports.db" 

# Directory structure (use absolute path if needed)
base_dir = r"C:\Users\A.I\Documents\Tatweer\Project 2\Reports"

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
    "ميزان المدفوعات",
    "بيانات الإيراد والإنفاق",
    "تقارير رقابية",
    "تقارير سنوية",
    "عمليات السوق",
    "ميزان المدفوعات",
    "أداء المصارف الليبية",
]

def extract_year(file_name):
    # Find all 4-digit sequences
    years = re.findall(r'(?<!\d)(\d{4})(?!\d)', file_name)
    
    # Convert to integers and filter valid years
    valid_years = [int(year) for year in years if 1900 <= int(year) <= 2100]
    
    # Return the latest year if available
    return str(max(valid_years)) if valid_years else 'عام'

with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()

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

    for folder in folders:
        report_type = folder
        folder_path = os.path.join(base_dir, folder)

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

print("Database created and populated.")


# Example usage (querying and handling NULL years):
with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reports WHERE year IS NOT NULL")  
    results = cursor.fetchall()

    for row in results:
        year = row[2] 
        print(row)
import streamlit as st
import sqlite3
import pandas as pd

# Database connection
DB_PATH =r"C:\Users\A.I\Documents\Tatweer\Project 2\Database\reports.db"

# Load data from database
def load_data():
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT id, report_type, year, name FROM reports"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Load file data from database
# def load_file(file_id):
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
    
#     # Log the query being executed
#     st.write(f"Executing query: SELECT name, file FROM reports WHERE id = {file_id}")

#     # Execute the query
#     cursor.execute("SELECT name, file FROM reports WHERE id = ?", (file_id,))
    
#     result = cursor.fetchone()
    
#     # Log the query result
#     st.write(f"Query Result: {result}")

#     conn.close()
#     if result:
#         return result
#     return None, None

def load_file(file_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Fetch all rows and filter in Python
    cursor.execute("SELECT id, name, file FROM reports")
    all_rows = cursor.fetchall()

    # Debugging: Print all rows
    # print(f"All Rows: {all_rows}")

    conn.close()

    # Find the row matching the file_id
    for row in all_rows:
        if row[0] == file_id:  # Match id
            file_name, file_content = row[1], row[2]
            return file_name, file_content

    return None, None


# Streamlit UI
st.title("Report Viewer")

# Load data
data = load_data()

# General Filters
report_types = ["All"] + sorted(data["report_type"].unique())
selected_type = st.selectbox("Select Report Type", report_types)

if selected_type != "All":
    data = data[data["report_type"] == selected_type]

years = ["All"] + sorted(data["year"].unique())
selected_year = st.selectbox("Select Year", years)

if selected_year != "All":
    data = data[data["year"] == selected_year]

# File Filter
file_names = data["name"].tolist()
selected_file = st.selectbox("Select a File", ["None"] + file_names)

if selected_file != "None":
    # Get file details
    file_id = data[data["name"] == selected_file]["id"].values[0]
    # st.write(f"Selected File ID: {file_id}, File Name: {selected_file}")  # Debugging output
    
    file_name, file_content = load_file(file_id)

    if file_name and file_content:
        st.subheader(f"Previewing: {file_name}")
        with st.expander("File Content"):
            if file_name.lower().endswith(".md"):
                st.markdown(file_content.decode("utf-8"), unsafe_allow_html=True)
            elif file_name.lower().endswith((".txt", ".csv")):
                st.text(file_content.decode("utf-8"))
            elif file_name.lower().endswith((".jpg", ".jpeg", ".png")):
                st.image(file_content)
            else:
                st.write("File format not supported for preview.")
    else:
        st.error("File not found in the database.")

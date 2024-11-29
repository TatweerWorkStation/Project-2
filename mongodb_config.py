import os
import base64
from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB (adjust the connection string if necessary)
client = MongoClient("mongodb://localhost:27017/")  # Adjust your connection string if needed
db = client["reports_database"]  # Database name
collection = db["reports"]  # Collection name

def extract_year(file_name):
    """
    Extract the year from the file name. Assuming the year is part of the file name.
    Modify this function based on your file naming conventions.
    """
    try:
        # Extract year as the first 4 digits from the file name
        year = int(''.join([char for char in file_name if char.isdigit()])[:4])
        return year
    except ValueError:
        return None  # Return None if no valid year can be extracted

def ingest_data_to_mongo(base_dir, chunk_size=10):
    """
    Reads files from the specified directory structure and uploads them to MongoDB in chunks.
    """
    # Get all subfolders (report types) from the 'Reports' directory
    for folder in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder)

        if os.path.isdir(folder_path):
            report_type = folder  # Report type is the folder name
            documents = []  # List to hold documents before bulk upload

            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                base_name, ext = os.path.splitext(file_name)

                # Only process .pdf and .md files
                if ext == ".pdf" or ext == ".md":
                    try:
                        # Read the file and encode it as base64
                        with open(file_path, "rb") as file:
                            file_data = file.read()
                        encoded_data = base64.b64encode(file_data).decode('utf-8')

                        # Extract the year (customize extraction based on your file name)
                        year = extract_year(base_name)

                        # Create the document structure
                        document = {
                            "id": f"{folder}_{base_name}",  # Unique ID based on folder (report type) and base name
                            "report_type": report_type,
                            "year": year,
                            "name": base_name,
                            f"{ext[1:]}_file": encoded_data  # Store the encoded file (pdf_file or md_file)
                        }

                        # Append document to the batch list
                        documents.append(document)

                        # If we've reached the chunk size, upload the batch to MongoDB
                        if len(documents) >= chunk_size:
                            collection.insert_many(documents)  # Insert the chunk of documents
                            documents.clear()  # Clear the list for the next batch

                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")

            # Insert any remaining documents after the loop
            if documents:
                collection.insert_many(documents)

    print("Data ingestion to MongoDB completed.")

# Example usage:
base_directory = "Reports"  # Folder where the report type folders are stored
ingest_data_to_mongo(base_directory, chunk_size=10)  # Process in chunks of 10 files

# تقارير مصرف ليبيا المركزي - أداة التلخيص

This Streamlit application provides a user-friendly interface for browsing, viewing, and summarizing reports from the Central Bank of Libya. It leverages both a local LLM (like Llama) and Google's Gemini API for text summarization in Arabic.

## Features

* **Interactive Filtering:** Easily filter reports by type and year.
* **Text Display:** View the full text of selected reports.
* **Dual Summarization Options:** Generate summaries using either a local LLM or the Gemini API.
* **Arabic Language Support:** The entire application, including summarization, is tailored for Arabic text.
* **Clean and Modern UI:** Utilizes custom CSS for an enhanced user experience.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
Use code with caution.
Markdown
Install required packages:

pip install -r requirements.txt
Use code with caution.
Bash
Set up your environment:

Create a .env file in the root directory and add your Google API key:

GOOGLE_API_KEY=YOUR_ACTUAL_API_KEY

Ensure your local LLM server is running at http://127.0.0.1:1234.

Run the app:

streamlit run main.py

Choose a specific report file.

Click "عرض النص" to display the full report text.

Click "تلخيص النص (Llama)" or "تلخيص النص (Gemini)" to generate a summary using the respective model.

Project Structure
├── Database/      # Contains the SQLite database file (reports.db)
├── Images/       # Contains image files, including the logo
├── Reports/       # Directory for storing report files, if needed
├── .env           # Environment variables (Google API Key)
├── .gitignore      # Files and directories to exclude from Git
├── Asistant_Prompt.txt  # (Optional) Prompts or instructions for the LLM
├── database_script.py   # Script for setting up the database
├── config.py        # Main Streamlit application logic code
└── config.py        # Main Streamlit UI code
Database Setup
The database_script.py file is used to create and populate the SQLite database. Make sure to run this script before using the application if the database doesn't exist or needs to be updated.


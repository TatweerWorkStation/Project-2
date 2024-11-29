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

2. **Prerequistes:**
Install required packages:

`pip install -r requirements.txt`

Set up your environment:

Create a .env file in the root directory and add your Google API key:

`GOOGLE_API_KEY=YOUR_ACTUAL_API_KEY`

Ensure your local LLM server is running at http://127.0.0.1:1234.

Run database_pandas by executing `python database_pandas.py`. Do this only once, it will create a reports.csv file with references to every file in the database.

3. **Run the app:**

`streamlit run main.py`

Choose a specific report file.

Click "عرض النص" to display the full report text.

Click "تلخيص النص (Llama)" or "تلخيص النص (Gemini)" to generate a summary using the respective model.

# Project Structure

- **Database/**        # Contains the SQLite database file (`reports.db`)
- **Images/**          # Contains image files, including the logo
- **Reports/**         # Directory for storing report files, if needed
- **.env**             # Environment variables (Google API Key)
- **.gitignore**       # Files and directories to exclude from Git
- **Asistant_Prompt.txt**  # (Optional) Prompts or instructions for the LLM
- ~database_script.py # Script for setting up the database~
- **database_pandas.py**   # Script for setting up the database
- **config.py**        # Main Streamlit application logic code
- **config.py**        # Main Streamlit UI code (Note: Duplicate `config.py`)
Database Setup
The database_pandas.py file is used to create and populate the csv file. Make sure to run this script before using the application if the database doesn't exist or needs to be updated.



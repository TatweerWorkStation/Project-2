# تقارير مصرف ليبيا المركزي - أداة التلخيص

This Streamlit application provides a user-friendly interface for browsing, viewing, and summarizing reports from the Central Bank of Libya.  It leverages both a local LLM (like Llama) and Google's Gemini API for text summarization in Arabic.

## Features

* **Interactive Filtering:** Easily filter reports by type and year.
* **Text Display:** View the full text of selected reports.
* **Dual Summarization Options:** Generate summaries using either a local LLM or the Gemini API.
* **Arabic Language Support:** The entire application, including summarization, is tailored for Arabic text.
* **Clean and Modern UI:**  Utilizes custom CSS for an enhanced user experience.


## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
content_copy
Use code with caution.
Markdown

Install required packages:

pip install -r requirements.txt
content_copy
Use code with caution.
Bash

Set up your environment:

Create a .env file in the root directory and add your Google API key:

GOOGLE_API_KEY=YOUR_ACTUAL_API_KEY
content_copy
Use code with caution.

Ensure your local LLM server is running at http://127.0.0.1:1234. (Adjust the URL in main.py if necessary.)

Run the app:

streamlit run main.py
content_copy
Use code with caution.
Bash
Usage

Select the report type and year using the dropdown menus.

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
└── main.py        # Main Streamlit application code
content_copy
Use code with caution.
Database Setup

The database_script.py file is used to create and populate the SQLite database. Make sure to run this script before using the application if the database doesn't exist or needs to be updated.

Contributing

Contributions are welcome! Feel free to open issues and pull requests.

License

[Specify your license here, e.g., MIT]

Key improvements:

* Clearer explanations of features and installation steps.
* Detailed project structure description.
* Information about database setup.
* Placeholder for license information.
* Arabic titles and descriptions where relevant, matching the application's language.
* Emphasis on the dual summarization options (Llama and Gemini).
* Instructions for setting up the `.env` file.
*  A more visually appealing layout using Markdown formatting.
content_copy
Use code with caution.

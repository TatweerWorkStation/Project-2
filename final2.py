import streamlit as st
import requests
import sqlite3
import pandas as pd

# Database connection
DB_PATH = r"C:\Users\A.I\Documents\Tatweer\Project 2\Database\reports.db"

# Load data from the database
def load_data():
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT id, report_type, year, name FROM reports"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

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


# Summarize text using the local LLM server
def summarize_text(text):
    try:
        url = "http://127.0.0.1:1234/v1/chat/completions"
        payload = {
            "model": "meta-llama-3.1-8b-instruct",
            "messages": [
                {"role": "system", "content": "Always answer in bullet points."},
                {"role": "user", "content": f'قم بتخليص الملف التالي باللغة العربية: {text}'}],
            "temperature": 0,
            "max_tokens": 512,
            "stream": False
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:  # Catch request-related errors
        return f"Error communicating with LLM server: {e}"
    except (KeyError, IndexError) as e:  # Catch errors in response parsing
        return f"Error parsing LLM response: {e}"
    except Exception as e:  # Catch any other exceptions
        return f"An unexpected error occurred: {e}"

# Streamlit UI Configuration
st.set_page_config(
    page_title="ملخص التقارير",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject custom CSS for styling with enhanced aesthetics
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
        body {
            font-family: 'Tajawal', sans-serif;
            direction: rtl;
            text-align: right;
            background-color: #f8f9fa; /* Light background */
            color: #343a40; /* Dark text for contrast */
        }
        .stApp {
            background-color: #f8f9fa;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #2e5984; /* Primary color for headers */
            font-weight: 700;
        }
        .stButton button {
            background-color: #2e5984; /* Primary color for buttons */
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 18px;
            font-weight: 500;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: background-color 0.3s, transform 0.2s;
            margin: 5px 0;
        }
        .stButton button:hover {
            background-color: #234b6e; /* Darker shade on hover */
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
        }
        .stSelectbox, .stTextArea textarea {
            border-radius: 8px;
            border: 1px solid #ced4da;
            padding: 10px 15px;
            margin-bottom: 15px;
            font-size: 16px;
            direction: rtl;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: border-color 0.3s;
        }
        .stSelectbox:focus-within, .stTextArea textarea:focus-within {
            border-color: #2e5984;
            box-shadow: 0 2px 6px rgba(46, 89, 132, 0.3);
        }
        .report-container {
            background-color: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 6px 12px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .summary-box {
            border: 1px solid #e0e0e0;
            padding: 18px;
            border-radius: 12px;
            margin-top: 15px;
            background-color: #f0f4f8; /* Light blue background for summary */
        }
        .st-emotion-cache-zq5a9r { /* Adjust padding for main area */
            padding: 2rem;
        }
        hr {
            border-color: #2e5984;
            margin-top: 10px;
            margin-bottom: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Load data and setup filters
data = load_data()
st.title("ملخص التقارير")
st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    selected_year = st.selectbox("اختر السنة", options=sorted(set(data["year"]), reverse=True))
with col2:
    filtered_data_year = data[data["year"] == selected_year]
    selected_type = st.selectbox("اختر نوع التقرير", options=sorted(set(filtered_data_year["report_type"])))
with col3:
    final_filtered_data = filtered_data_year[filtered_data_year["report_type"] == selected_type]
    selected_file = st.selectbox("اختر الملف", options=final_filtered_data["name"].tolist())

# File Action Buttons
col4, col5 = st.columns(2)
with col4:
    display_button_clicked = st.button("عرض النص")
with col5:
    summarize_button_clicked = st.button("تلخيص النص")

# Main Content Area
if selected_file:
    file_id = final_filtered_data[final_filtered_data["name"] == selected_file]["id"].values[0]
    file_name, file_content = load_file(file_id)

    if file_content:
        if file_name.lower().endswith((".txt", ".md", ".csv")):
            text_content = file_content.decode("utf-8")

            if display_button_clicked:
                st.session_state.extracted_text = text_content
                st.subheader("النص الكامل")
                st.markdown(f"<div class='report-container'><p>{text_content}</p></div>", unsafe_allow_html=True)

            if summarize_button_clicked:
                if 'extracted_text' in st.session_state:
                    with st.spinner('انتظر قليلا يتم التلخيص...'):
                         summary = summarize_text(st.session_state.extracted_text)
                    st.subheader("الملخص")
                    st.markdown(f"<div class='report-container summary-box'><p>{summary}</p></div>", unsafe_allow_html=True)
                else:
                    st.warning
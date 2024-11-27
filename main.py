import streamlit as st
import requests
import sqlite3
import pandas as pd
import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
# Gemini API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)  # Replace with your actual key
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# Database connection
DB_PATH = r"C:\Users\A.I\Documents\Tatweer\Project 2\Database\reports.db"

def load_data():  # Ensure this function is correctly defined in your file
    conn = sqlite3.connect(DB_PATH)
    try:
        query = "SELECT id, report_type, year, name FROM reports"
        df = pd.read_sql_query(query, conn)
        return df
    except pd.io.sql.DatabaseError as e:
        st.error(f"Database error: {e}")  # Handle potential database errors
        return pd.DataFrame()  # Return empty DataFrame on error
    finally:
        conn.close()

def load_file(file_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name, file FROM reports")
        rows = cursor.fetchall()
        for row in rows:
            if row[0] == file_id:  # Match id
                file_name, file_content = row[1], row[2]
                return file_name, file_content
        return None, None
    except sqlite3.Error as e:  # Handle SQLite errors
        st.error(f"Database error: {e}")
        # return None, None
    finally:
        conn.close()


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
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error communicating with LLM server: {e}"
    except (KeyError, IndexError) as e:
        return f"Error parsing LLM response: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"



# Summarize text using Gemini API
def summarize_text_gemini(text):
    try:
        response = gemini_model.generate_content(f"  قم بتلخيص النص التالي باللغة العربية مع استخدام نقاط منظمة {text}")
        return response.text
    except Exception as e:
        return f"Error summarizing with Gemini: {e}"


# Streamlit UI Configuration
st.set_page_config(
    page_title="ملخص التقارير",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Use columns to center the image
col1, col2, col3, = st.columns([1, 1, 1])

with col3:
    st.image("Images\logo_b.png", width=300)
with col1:
    st.title("ملخص التقارير")
# Inject custom CSS for styling with enhanced aesthetics
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
        * {
            font-family: 'Tajawal', sans-serif;
        }
        body {
            direction: rtl;
            text-align: right;
            background-color: #f8f9fa;
            color: #343a40;
        }
        .stApp {
            background-color: #f8f9fa;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #000;
            font-weight: 700;
        }
        .stButton button {
            background-color: #000;
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
            # transform: translateY(-2px);
            color: white !important
      
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
            border-color: #000;
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
            background-color: #f0f4f8;
        }
        .st-emotion-cache-zq5a9r {
            padding: 2rem;
        }
        hr {
            border-color: #000;
            margin-top: 10px;
            margin-bottom: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Load data and setup filters
data = load_data()
# st.title("ملخص التقارير")


col1, col2, col3 = st.columns(3)
with col1:
    selected_type = st.selectbox("اختر نوع التقرير", options=sorted(set(data["report_type"])))
with col2:
    filtered_data_type = data[data["report_type"] == selected_type]
    selected_year = st.selectbox("اختر السنة", options=sorted(set(filtered_data_type["year"]), reverse=True))
with col3:
    final_filtered_data = filtered_data_type[filtered_data_type["year"] == selected_year]
    selected_file = st.selectbox("اختر الملف", options=final_filtered_data["name"].tolist() if not final_filtered_data.empty else ['لا يوجد ملفات'])


# File Action Buttons (Modified)
col4, col5, col6 = st.columns(3) # Added a third column
with col4:
    display_button_clicked = st.button("عرض النص")
with col5:
    summarize_button_clicked = st.button("تلخيص النص (Llama)")
with col6:
    summarize_button_gemini_clicked = st.button("تلخيص النص (Gemini)")

# Main Content Area
if selected_file and selected_file != 'لا يوجد ملفات':
    file_id = final_filtered_data[final_filtered_data["name"] == selected_file]["id"].values[0]
    file_name, file_content = load_file(file_id)
    if file_content:
        if file_name.lower().endswith((".txt", ".md", ".csv")):
            text_content = file_content.decode("utf-8")


            # Display Text Content
            if display_button_clicked:
                st.subheader("النص الكامل")
                st.markdown(f"<div class='report-container'><p>{text_content}</p></div>", unsafe_allow_html=True)
            
             # Summarize Text Content

       # Summarize Text Content (Llama)
            if summarize_button_clicked:
                summary = summarize_text(text_content)
                st.subheader("الملخص (Llama)")
                st.markdown(f"<div class='report-container summary-box'><p>{summary}</p></div>", unsafe_allow_html=True)

            # Summarize Text Content (Gemini)
            if summarize_button_gemini_clicked:
                summary_gemini = summarize_text_gemini(text_content)
                st.subheader("الملخص (Gemini)")
                st.markdown(f"<div class='report-container summary-box'><p>{summary_gemini}</p></div>", unsafe_allow_html=True)
    
elif selected_file == 'لا يوجد ملفات':
    st.warning("لا يوجد ملفات لهذا النوع والسنة")
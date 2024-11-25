import streamlit as st
import google.generativeai as genai
import os
import PyPDF2
import pdfplumber
import pandas as pd
from bidi.algorithm import get_display


# from langchain.document_loaders import PyPDFLoader, DirectoryLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter

# Set page configuration
st.set_page_config(page_title="Report Dashboard", layout="wide")

# Setting Up Gemeni API
genai.configure(api_key="AIzaSyBatPjf_Xykvv8b8_0HClSYpIrrGFPSFUA")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Write a story about a magic backpack.")

# def file_preprocessing(file):
#     loader =  PyPDFLoader(file)
#     pages = loader.load_and_split()
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
#     texts = text_splitter.split_documents(pages)
#     final_texts = ""
#     for text in texts:
#         print(text)
#         final_texts = final_texts + text.page_content
#     return final_texts

def extract_pdf_text(file):
    """Extract text from a PDF file."""
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"An error occurred: {e}"

# import pdfplumber
# import pandas as pd
# import arabic_reshaper
# from bidi.algorithm import get_display

# def reshape_arabic_text(text):
#     """Reshape Arabic text for proper display."""
#     reshaped_text = arabic_reshaper.reshape(text)  # Fix the letters
#     return get_display(reshaped_text)  # Apply bidirectional algorithm

# def extract_text_and_tables_to_string(pdf_file):
#     """Extract text and tables from a PDF and combine them into a single string."""
#     combined_content = ""
    
#     with pdfplumber.open(pdf_file) as pdf:
#         for page_number, page in enumerate(pdf.pages, start=1):
#             # Extract text from the page
#             text = page.extract_text()
#             if text:
#                 # Handle Arabic text
#                 reshaped_text = "\n".join([
#                     reshape_arabic_text(line) if any("ء" <= char <= "ي" for char in line) else line
#                     for line in text.splitlines()
#                 ])
#                 combined_content += f"--- Page {page_number}: Text ---\n{reshaped_text}\n\n"
            
#             # Extract tables from the page
#             tables = page.extract_tables()
#             if tables:
#                 for table_index, table in enumerate(tables, start=1):
#                     df = pd.DataFrame(table[1:], columns=table[0])  # Convert table to DataFrame
#                     combined_content += f"--- Page {page_number}, Table {table_index} ---\n"
#                     combined_content += df.to_csv(index=False) + "\n\n"
    
#     return combined_content


# CSS for RTL alignment
st.markdown(
    """
    <style>
    body, [class^="st-"] {
        direction: rtl; /* Set the direction to Right-to-Left */
        text-align: right; /* Align text to the right */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Use columns to center the image
col1, col2, col3,col4,col5 = st.columns([1, 1, 1, 1, 1])

with col3:
    st.image("logo_b.png", width=300)


# Set the app title
st.title("لوحة تقارير")
st.header('')
# Horizontal layout for filter widgets
with st.container():
    col1,col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        report_type = st.selectbox("نوع التقرير", ["النشرة الاقتصادية", "تقارير سنوية", "ميزان المدفوعات الليبي", "إحصاءات نقدية ومصرفية", "بيانات الإيراد والإنفاق"])

    with col2:
        report_date = st.selectbox("السنة", [str(year) for year in range(2000, 2025)])

    with col4:
        st.button("مسح")  # Reset/Clear button for filters
        # CSS for styling the button
        st.markdown(
            """
            <style>
            .stButton > button {
                height: 50px; /* Adjust height to match other inputs */
                width: 50%; /* Full width of column */
                font-size: 16px; /* Make text size similar to other inputs */
                margin-top: 10px; /* Adjust top margin for alignment */
            }
            </style>
            """,
            unsafe_allow_html=True
)


# Main content area for displaying report summary
st.subheader('إختيار التقرير')
st.write("الرجاء رفع ملف")

# File uploader
c1,c2,c3=st.columns([1, 1, 1])
with c3:
    uploaded_file = st.file_uploader("اختر ملف PDF", type="pdf")

if uploaded_file is not None:
    with st.spinner("جاري التلخيص..."):
        pdf_text = extract_pdf_text(uploaded_file)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("قم بتخليص واختصار الملف التالي لأهم النقاط المذكورة  باللغة العربية "+pdf_text)
    
    # st.text_area("Extracted Text", response.text, height=500)


# Placeholder for report summary
summary_placeholder = st.empty()
summary_placeholder.info("الرجاء اختيار تقرير والضغط على الزر للتلخيص")

if st.button("تلخيص"):
    summary_placeholder.info(response.text)

# # Footer or additional info
# st.markdown(
#     """
#     ---
#     *تم تصميم هذه اللوحة لتسهيل تصفية وعرض التقارير. سيتم إضافة خاصية التلخيص في التحديثات المستقبلية.*
#     """,
#     unsafe_allow_html=True,
# )
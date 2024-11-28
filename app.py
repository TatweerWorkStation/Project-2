import streamlit as st
from config import load_data, load_file, summarize_text, summarize_text_gemini

# Set page configuration
st.set_page_config(
    page_title="تقارير مصرف ليبيا المركزي - أداة التلخيص",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Use columns to center the image
col1, col2, col3 = st.columns([1, 1, 1])

with col3:
    st.image("Images/logo.png")
with col1:
    st.markdown('<div class="title-column"><h1 class="page-title">تقارير مصرف ليبيا المركزي - أداة التلخيص</h1></div>', unsafe_allow_html=True)

data = load_data()

with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_type = st.selectbox("اختر نوع التقرير", options=sorted(set(data["report_type"])))
    with col2:
        filtered_data_type = data[data["report_type"] == selected_type]
        selected_year = st.selectbox("اختر السنة", options=sorted(set(filtered_data_type["year"]), reverse=True))
    with col3:
        final_filtered_data = filtered_data_type[filtered_data_type["year"] == selected_year]
        selected_file = st.selectbox("اختر الملف", options=final_filtered_data["name"].tolist() if not final_filtered_data.empty else ['لا يوجد ملفات'])

    col4, col5, col6 = st.columns(3)
    with col4:
        display_button_clicked = st.button("عرض النص")
    with col5:
        summarize_button_clicked = st.button("تلخيص النص (Llama)")
    with col6:
        summarize_button_gemini_clicked = st.button("تلخيص النص (Gemini)")

    if selected_file and selected_file != 'لا يوجد ملفات':
        file_id = final_filtered_data[final_filtered_data["name"] == selected_file]["id"].values[0]
        file_name, file_content = load_file(file_id)
        if file_content:
            text_content = file_content.decode("utf-8")

            if display_button_clicked:
                st.subheader("النص الكامل")
                st.markdown(f"<div class='report-container'><p>{text_content}</p></div>", unsafe_allow_html=True)

            if summarize_button_clicked:
                summary = summarize_text(text_content)
                st.subheader("الملخص (Llama)")
                st.markdown(f"<div class='report-container summary-box'><p>{summary}</p></div>", unsafe_allow_html=True)

            if summarize_button_gemini_clicked:
                summary_gemini = summarize_text_gemini(text_content)
                st.subheader("الملخص (Gemini)")
                st.markdown(f"<div class='report-container summary-box'><p>{summary_gemini}</p></div>", unsafe_allow_html=True)

    elif selected_file == 'لا يوجد ملفات':
        st.warning("لا يوجد ملفات لهذا النوع والسنة")

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
        body {
            direction: rtl;
            text-align: right;
            background-color: #f8f9fa;
            color: #343a40;
        }
        .stApp {
            padding-top: 60px;
        }
        .title-column {
            display: flex;
            justify-content: center;
        }
        .report-container {
            background-color: white;
            padding: 20px;
            border-radius: 12px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

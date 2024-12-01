import streamlit as st 
from config import load_data, load_md, load_pdf, summarize_text_gemini, summarize_text_gemini_stream
import base64

# Set page configuration
st.set_page_config(
    page_title="تقارير مصرف ليبيا المركزي - أداة التلخيص",
    layout="wide",
    initial_sidebar_state="collapsed" ,
    page_icon="Images/icon.png"
)

# Page Title and Logo
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown('<h1 classname="page-font">تقارير مصرف ليبيا المركزي - أداة التلخيص</h1>', unsafe_allow_html=True)

    
with col2:
    st.image("Images/logo2.png", use_container_width=True)

# Load Data
data = load_data()

# Filters Section
with st.container():
    col1, col2 = st.columns(2)   
    with col1:
        selected_type = st.selectbox(
            "اختر نوع التقرير",
            options=["عرض الكل"] + sorted(set(data["report_type"])),
            key="selected_type"
        )
    with col2:
        # Dynamically adjust available years based on the selected report type
        if st.session_state.get("selected_type") and st.session_state["selected_type"] != "عرض الكل":
            applicable_years = sorted(
                set(data[data["report_type"] == st.session_state["selected_type"]]["year"]),
                reverse=True
            )
        else:
            applicable_years = sorted(set(data["year"]), reverse=True)
        selected_year = st.selectbox("اختر السنة", options=["عرض الكل"] + applicable_years)

# Filter Data
filtered_data = data.copy()
if selected_year != "عرض الكل":
    filtered_data = filtered_data[filtered_data["year"] == selected_year]
if selected_type != "عرض الكل":
    filtered_data = filtered_data[filtered_data["report_type"] == selected_type]

# Files Table Section
st.markdown('<h3 classname="page-font mt-8">الملفات المتاحة</h3>', unsafe_allow_html=True)
if not filtered_data.empty:
    # Create a scrollable container for the table
    with st.container(height=300, border=False):
        for index, row in filtered_data.iterrows():
            col1, col2 = st.columns([4, 1])

            with col1:
                st.write(f"📄 {row['name']}")
            with col2:
                if st.button("عرض", key=f"display_{index}"):
                    st.session_state["selected_file_id"] = row["id"]
else:
    st.warning("لا يوجد ملفات متاحة لهذا النوع والسنة.")

# Bottom Section: PDF Viewer and Summary
st.markdown("---")
pdf_col, spacer_col, summary_col = st.columns([1, 0.1, 1])

with pdf_col:
    st.markdown('<h3 classname="page-font mt-8">عرض الملف</h3>', unsafe_allow_html=True)

    if "selected_file_id" in st.session_state:
        file_id = st.session_state["selected_file_id"]
        file_path = load_pdf(file_id)
        if file_path:
            try:
                with open(file_path, "rb") as pdf_file:
                    file_content = pdf_file.read()
                    base64_pdf = base64.b64encode(file_content).decode('utf-8')
                    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px"></iframe>'
                    st.markdown(pdf_display, unsafe_allow_html=True)
            except Exception as e:
                st.warning(f"تعذر تحميل الملف: {e}")
        else:
            st.warning("تعذر تحميل الملف. يرجى المحاولة مرة أخرى.")
    else:
        st.write("اضغط على 'عرض' لعرض الملف هنا.")

with summary_col:
    st.markdown('<h3 classname="page-font mt-8">الملخص</h3>', unsafe_allow_html=True)

    if "selected_file_id" in st.session_state:
        if st.button("تلخيص النص"):
            file_id = st.session_state["selected_file_id"]
            file_path = load_md(file_id)  # Load the file path

            # Check if file_path is a valid string (not an error message)
            if isinstance(file_path, str) and file_path:
                try:
                    # Open and read the markdown file
                    with open(file_path, "r", encoding="utf-8") as md_file:
                        text_content = md_file.read()

                    # Define the generator for streaming
                    summary_generator = summarize_text_gemini_stream(text_content)

                    # Display the summary using st.write_stream
                    with st.spinner("جارٍ تلخيص النص..."):
                        summary = st.write_stream(summary_generator)
                    st.success("تم تلخيص النص بنجاح.")

                except Exception as e:
                    st.warning(f"تعذر تحميل الملف: {e}")
            else:
                # If the file path is None or error message, show a warning
                st.warning(file_path)
    else:
        st.write("اضغط على 'عرض' ثم 'تلخيص النص' لعرض الملخص هنا.")

# Add CSS for better table styling
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
        * {
            font-family: 'Tajawal', sans-serif
        }
        body {
            direction: rtl;
            text-align: right;
        }
        .stApp {
            padding-top: 60px;
        }
        .page-font {
            font-family: 'Tajawal', sans-serif
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
        .mt-8 {
            margin-bottom: 8px
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
        }
        th {
            background-color: #f2f2f2;
            text-align: center;
        }
        td {
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True
)

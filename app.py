import streamlit as st 
from config import load_data, load_md, load_pdf , summarize_text_gemini_stream
import base64
from streamlit_pdf_viewer import pdf_viewer

st.set_page_config(
    page_title="Central Bank of Libya Reports - Summarization Tool",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="Images/icon.png"
)

# Language Selection
language = st.radio(
    "Select Language | اختر اللغة",
    options=["English", "Arabic"],
    index=1,
    horizontal=True
)

if language == "English":
    page_direction = "ltr"
    text_align = "left"
    page_title = "Central Bank of Libya Reports - Summarization Tool"
    reports_label = "Available Files"
    report_type_label = "Select Report Type"
    year_label = "Select Year"
    view_button_text = "View"
    summarize_button_text = "Summarize Text"
    summary_label = "Summary"
    file_display_label = "File Viewer"
    no_files_warning = "No files available for this type and year."
    load_error_message = "Failed to load the file. Please try again."
    loading_summary_message = "Summarizing the text..."
    summary_success_message = "Report summarized successfully."
    take_caution ='Summarization Tool can make mistakes. Check important info.'
else:
    page_direction = "rtl"
    text_align = "right"
    page_title = "تقارير مصرف ليبيا المركزي - أداة التلخيص"
    reports_label = "الملفات المتاحة"
    report_type_label = "اختر نوع التقرير"
    year_label = "اختر السنة"
    view_button_text = "عرض"
    summarize_button_text = "تلخيص النص"
    summary_label = "الملخص"
    file_display_label = "عرض الملف"
    no_files_warning = "لا يوجد ملفات متاحة لهذا النوع والسنة."
    load_error_message = "تعذر تحميل الملف. يرجى المحاولة مرة أخرى."
    loading_summary_message = "جاري تلخيص النص..."
    summary_success_message = "تم تلخيص التقرير بنجاح."
    take_caution ='.أداة التلخيص قد ترتكب أخطاء. تحقق من المعلومات المهمة'
    

st.markdown(
    f"""
    <style>
        body {{
            direction: {page_direction};
            text-align: {text_align};
        }}
        * {{
            font-family: 'Tajawal', sans-serif;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Page Title and Logo
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown(f'<h1 classname="page-font">{page_title}</h1>', unsafe_allow_html=True)

with col2:
    st.image("Images/logo3.png", use_container_width=True)

# Load Data
data = load_data()

# Filters Section
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        selected_type = st.selectbox(
            report_type_label,
            options=["All" if language == "English" else "عرض الكل"] + sorted(set(data["report_type"])),
            key="selected_type"
        )
    with col2:
        # Dynamically adjust available years based on the selected report type
        if st.session_state.get("selected_type") and st.session_state["selected_type"] != ("All" if language == "English" else "عرض الكل"):
            applicable_years = sorted(
                set(data[data["report_type"] == st.session_state["selected_type"]]["year"]),
                reverse=True
            )
        else:
            applicable_years = sorted(set(data["year"]), reverse=True)
        selected_year = st.selectbox(year_label, options=["All" if language == "English" else "عرض الكل"] + applicable_years)

# Filter Data
filtered_data = data.copy()
if selected_year != ("All" if language == "English" else "عرض الكل"):
    filtered_data = filtered_data[filtered_data["year"] == selected_year]
if selected_type != ("All" if language == "English" else "عرض الكل"):
    filtered_data = filtered_data[filtered_data["report_type"] == selected_type]

# Files Table Section
st.markdown(f'<h3 classname="page-font mt-8">{reports_label}</h3>', unsafe_allow_html=True)
if not filtered_data.empty:
    # Create a scrollable container for the table
    with st.container(height=300, border=False):
        for index, row in filtered_data.iterrows():
            col1, col2 = st.columns([4, 1])

            with col1:
                st.write(f"📄 {row['name']}")
            with col2:
                if st.button(view_button_text, key=f"display_{index}"):
                    st.session_state["selected_file_id"] = row["id"]
else:
    st.warning(no_files_warning)

# Bottom Section: PDF Viewer and Summary
st.markdown("---")
pdf_col, spacer_col, summary_col = st.columns([1, 0.1, 2])

with pdf_col:
    st.markdown(f'<h3 classname="page-font mt-8">{file_display_label}</h3>', unsafe_allow_html=True)

    if "selected_file_id" in st.session_state:
        file_id = st.session_state["selected_file_id"]
        file_path = load_pdf(file_id)
        if file_path:
            try:
                with open(file_path, "rb") as pdf_file:
                    pdf_viewer(input=file_path, width=700, height=600,resolution_boost=8)  # Set custom width and height

            except Exception as e:
                st.warning(f"{load_error_message}: {e}")
        else:
            st.warning(load_error_message)
    else:
        st.write(f"Press '{view_button_text}' to view the file here." if language == "English" else "اضغط على 'عرض' لعرض الملف هنا.")

with summary_col:
    st.markdown(f'<h3 classname="page-font mt-8">{summary_label}</h3>', unsafe_allow_html=True)

    summary_css = (
        """
        <style>
            .stVerticalBlock.st-emotion-cache-2awdga.e1f1d6gn2 {
                direction: ltr;
                text-align: left;
            }
        </style>
        """
        if language == "English"
        else """
        <style>
            .stVerticalBlock.st-emotion-cache-2awdga.e1f1d6gn2 {
                direction: rtl !important;
                text-align: right !important;
            }
        </style>
        """
    )
    st.markdown(summary_css, unsafe_allow_html=True)

    # Wrapper div for summary section
    st.markdown('<div class="summary-section">', unsafe_allow_html=True)

    if "selected_file_id" in st.session_state:
        if st.button(summarize_button_text):
            file_id = st.session_state["selected_file_id"]
            file_path = load_md(file_id)  # Load the file path

            # Check if file_path is a valid string (not an error message)
            if isinstance(file_path, str) and file_path:
                try:
                    # Open and read the markdown file
                    with open(file_path, "r", encoding="utf-8") as md_file:
                        text_content = md_file.read()

                    # Define the generator for streaming
                    summary_generator = summarize_text_gemini_stream(text_content, language)

                    # Display the summary using st.write_stream
                    with st.spinner(loading_summary_message):
                        summary = st.write_stream(summary_generator)
                    # st.success(summary_success_message)
                    st.warning (take_caution)
                    st.toast(summary_success_message,icon='✅')
                except Exception as e:
                    st.warning(f"{load_error_message}: {e}")
            else:
                # If the file path is None or error message, show a warning
                st.warning(file_path)
    else:
        st.write(
            f"Press '{view_button_text}' then '{summarize_button_text}' to view the summary here."
            if language == "English"
            else "اضغط على 'عرض' ثم 'تلخيص النص' لعرض الملخص هنا."
        )

    # Close the wrapper div
    st.markdown('</div>', unsafe_allow_html=True)


# Add CSS for better table styling
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
        * {
            font-family: 'Tajawal'
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
st.markdown(
    f"""
    <style>
    body {{
        direction: {page_direction};
        text-align: {text_align};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

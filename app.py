# app.py
import streamlit as st 
from config import load_data, load_md, load_pdf, summarize_text_gemini_stream, summarize_multiple_documents_gemini_stream
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
    summarize_multiple_button_text = "Summarize Selected"
    summary_label = "Summary"
    file_display_label = "File Viewer"
    no_files_warning = "No files available for this type and year."
    load_error_message = "Failed to load the file. Please try again."
    loading_summary_message = "Summarizing the text..."
    summary_success_message = "Report summarized successfully."
    take_caution = 'Summarization Tool can make mistakes. Check important info.'
    select_documents_label = "Select Documents"
    select_all_label = "Select All"
    inconsistent_type_warning = "Please select documents from the same report type."
else:
    page_direction = "rtl"
    text_align = "right"
    page_title = "تقارير مصرف ليبيا المركزي - أداة التلخيص"
    reports_label = "الملفات المتاحة"
    report_type_label = "اختر نوع التقرير"
    year_label = "اختر السنة"
    view_button_text = "عرض"
    summarize_button_text = "تلخيص النص"
    summarize_multiple_button_text = "تلخيص المحدد"
    summary_label = "الملخص"
    file_display_label = "عرض الملف"
    no_files_warning = "لا يوجد ملفات متاحة لهذا النوع والسنة."
    load_error_message = "تعذر تحميل الملف. يرجى المحاولة مرة أخرى."
    loading_summary_message = "جاري تلخيص النص..."
    summary_success_message = "تم تلخيص التقرير بنجاح."
    take_caution = '.أداة التلخيص قد ترتكب أخطاء. تحقق من المعلومات المهمة'
    select_documents_label = "اختر المستندات"
    select_all_label = "اختر الكل"
    inconsistent_type_warning = "يرجى اختيار مستندات من نفس نوع التقرير."

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
    st.markdown(f'<h1 class="page-font">{page_title}</h1>', unsafe_allow_html=True)

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

# Initialize session state for selected files
if "selected_file_ids" not in st.session_state:
    st.session_state["selected_file_ids"] = []

# Files Table Section
st.markdown(f'<h3 class="page-font mt-8">{reports_label}</h3>', unsafe_allow_html=True)
if not filtered_data.empty:
    st.markdown("---")
    with st.container(height=300, border=False):
        
        st.markdown('<div class="report-container">', unsafe_allow_html=True)
        
        # Display each report with a checkbox and view button
        for index, row in filtered_data.iterrows():
            cols = st.columns([0.1, 0.6, 0.3])
            with cols[0]:
                is_checked = row["id"] in st.session_state["selected_file_ids"]
                if st.checkbox("", key=f"select_{row['id']}", value=is_checked):
                    if row["id"] not in st.session_state["selected_file_ids"]:
                        st.session_state["selected_file_ids"].append(row["id"])
                else:
                    if row["id"] in st.session_state["selected_file_ids"]:
                        st.session_state["selected_file_ids"].remove(row["id"])
            with cols[1]:
                st.write(f"📄 {row['name']}")
            with cols[2]:
                if st.button(view_button_text, key=f"display_{row['id']}"):
                    st.session_state["selected_file_ids"] = [row["id"]]
        
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.warning(no_files_warning)

# Validate selected documents
selected_file_ids = st.session_state.get("selected_file_ids", [])
valid_selection = True
if len(selected_file_ids) > 1:
    selected_types = filtered_data[filtered_data["id"].isin(selected_file_ids)]["report_type"].unique()
    if len(selected_types) > 1:
        valid_selection = False
        st.toast(inconsistent_type_warning)
        #st.error(inconsistent_type_warning)
elif len(selected_file_ids) == 1:
    valid_selection = True
else:
    valid_selection = False

# Bottom Section: PDF Viewer and Summary
st.markdown("---")
pdf_col, spacer_col, summary_col = st.columns([1, 0.1, 2])

with pdf_col:
    st.markdown(f'<h3 class="page-font mt-8">{file_display_label}</h3>', unsafe_allow_html=True)

    if "selected_file_ids" in st.session_state and len(st.session_state["selected_file_ids"]) > 0:
        file_id = st.session_state["selected_file_ids"][0]
        file_path = load_pdf(file_id)
        if file_path:
            try:
                pdf_viewer(input=file_path, width=700, height=600, resolution_boost=8)  # Set custom width and height
            except Exception as e:
                st.warning(f"{load_error_message}: {e}")
        else:
            st.warning(load_error_message)
    else:
        st.write(
            f"Press '{view_button_text}' to view the file here." if language == "English" else "اضغط على 'عرض' لعرض الملف هنا."
        )

with summary_col:
    st.markdown(f'<h3 class="page-font mt-8">{summary_label}</h3>', unsafe_allow_html=True)

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

    if selected_file_ids:
        # Disable the summarize button if selection is invalid
        disable_button = not valid_selection
        if disable_button:
            button_disabled = True
        else:
            button_disabled = False

        # Display the summarize button with disabled state
        summarize_button = st.button(
            summarize_multiple_button_text,
            disabled=disable_button
        )

        if summarize_button and not disable_button:
            file_paths = [load_md(fid) for fid in selected_file_ids]

            # Check if all file_paths are valid strings
            if all(isinstance(fp, str) and fp for fp in file_paths):
                try:
                    # Open and read all markdown files
                    texts = []
                    for fp in file_paths:
                        with open(fp, "r", encoding="utf-8") as md_file:
                            texts.append(md_file.read())

                    # Define the generator for streaming
                    summary_generator = summarize_multiple_documents_gemini_stream(texts, language)

                    # Display the summary using st.write_stream
                    with st.spinner(loading_summary_message):
                        summary = st.write_stream(summary_generator)
                    st.warning(take_caution)
                    st.toast(summary_success_message, icon='✅')
                except Exception as e:
                    st.warning(f"{load_error_message}: {e}")
            else:
                # If any file path is None or error message, show a warning
                st.warning(
                    "One or more selected files could not be loaded." 
                    if language == "English" 
                    else "تعذر تحميل واحد أو أكثر من الملفات المحددة."
                )
    else:
        st.write(
            f"Select documents and click '{summarize_multiple_button_text}' to view the summary here."
            if language == "English"
            else f"اختر المستندات وانقر على '{summarize_multiple_button_text}' لعرض الملخص هنا."
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
            padding: 10px;
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

# config.py
import os
import google.generativeai as genai
from dotenv import load_dotenv
import pandas as pd
import requests
import re

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
gemini_model = genai.GenerativeModel("gemini-2.0-flash-exp")

CSV_FILE_PATH = os.path.join(os.getcwd(), "reports.csv")

def load_data():
    try:
        df = pd.read_csv(CSV_FILE_PATH)
        return df
    except Exception as e:
        return f"Error with CSV file: {e}"  # Return error message if any issue occurs

def load_pdf(file_id):
    """
    Loads the PDF file path from the CSV file based on the file ID.
    """
    try:
        df = pd.read_csv(CSV_FILE_PATH)
        file_path = df.loc[df['id'] == file_id, 'pdf_path'].squeeze()
        if not pd.isna(file_path):
            return file_path
        return None
    except Exception as e:
        return f"Error with CSV file: {e}"

def load_md(file_id):
    """
    Loads the MD file path from the CSV file based on the file ID.
    """
    try:
        df = pd.read_csv(CSV_FILE_PATH)
        row = df[df['id'] == file_id]
        
        if not row.empty:
            file_path = row.iloc[0]['md_path']
            return file_path
        return None
    except Exception as e:
        return f"Error with CSV file: {e}", None

def summarize_text_gemini_stream(text, language):
    """
    Summarizes the given text using Gemini, with streaming support.
    The summary will be in the specified language (English or Arabic).
    """
    try:
        if language == "English":
            prompt = f"""
            Summarize the following text in English using organized headings and bullet points.
            Add Markdown tables for key data if applicable.
            {text}
            """
        else:  # Default to Arabic
            prompt = f"""
            قم بتلخيص النص التالي باللغة العربية مع استخدام نقاط وعناوين منظمة وشاملة.
            إذا كان ذلك مناسبًا، أضف جداول بتنسيق Markdown لعرض البيانات الهامة.
            {text}
            """

        response = gemini_model.generate_content(prompt, stream=True)
        buffer = []
        table_pattern = re.compile(r'(\|.*\|\n)+(\|[-|]+\|)+(\|.*\|)+')
        for chunk in response:
            if hasattr(chunk, 'text'):
                chunk_text = chunk.text
                buffer.append(chunk_text)
                
                current_text = ''.join(buffer)
                matches = table_pattern.findall(current_text)
                
                if matches:
                    complete_table = matches[-1][0]
                    yield complete_table
                    buffer = []
                else:
                    yield chunk_text
            else:
                yield ""
    except Exception as e:
        yield f"Error in summarization: {e}" if language == "English" else f"يوجد خلل في التلخيص : {e}"

def summarize_multiple_documents_gemini_stream(texts, language):
    """
    Summarizes multiple documents using Gemini, generating a unified summary.
    """
    try:
        if language == "English":
            prompt = f"""
            Generate a unified summary that coherently connects information from the following texts.
            Include comparative tables for numerical data.
            Highlight key findings and patterns.
            
            Texts:
            {"".join([f"Document {i+1}:\n{text}\n" for i, text in enumerate(texts)])}
            """
        else:
            prompt = f"""
            قم بإنشاء ملخص موحد يربط بشكل متماسك المعلومات من النصوص التالية.
            أضف جداول مقارنة للبيانات العددية.
            أبرز النتائج الرئيسية والأنماط.
            
            النصوص:
            {"".join([f"المستند {i+1}:\n{text}\n" for i, text in enumerate(texts)])}
            """

        response = gemini_model.generate_content(prompt, stream=True)
        buffer = []
        table_pattern = re.compile(r'(\|.*\|\n)+(\|[-|]+\|)+(\|.*\|)+')
        for chunk in response:
            if hasattr(chunk, 'text'):
                chunk_text = chunk.text
                buffer.append(chunk_text)
                
                current_text = ''.join(buffer)
                matches = table_pattern.findall(current_text)
                
                if matches:
                    complete_table = matches[-1][0]
                    yield complete_table
                    buffer = []
                else:
                    yield chunk_text
            else:
                yield ""
    except Exception as e:
        yield f"Error in summarization: {e}" if language == "English" else f"يوجد خلل في التلخيص : {e}"

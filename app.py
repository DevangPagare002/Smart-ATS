import streamlit
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import PyPDF2 as pdf

load_dotenv() ## Load my environment variables.

genai.configure(api_key = os.getenv("GOOGLE_API_KEY")) ## Configuring the API key

def get_gemini_response(input):
    model = genai.GenerativeModel("gemini-pro") ## Calling Gemini model
    response = model.generate_content(input)
    response = json.loads(response.text)
    return response

def read_text_from_pdf(uploaded_files):
    reader = pdf.PdfReader(uploaded_files) ## Read the pdf
    text = ""
    for page in range(len(reader.pages)): ## Loop over each page
        page = reader.pages[page]
        text += str(page.extract_text()) ## Append page-text into text variable

    return text

input_prompt = """
Hii, Act like you are a very skillful or experienced ATS(Application Tracking System).
You have deep understanding of tech field, spftware engineering, data science, data analysis and big data
engineer. Your task is to evaluate the resume based on given job description.
You must consider that the job market is very competitive and you should provide bjest assistance for improving the resume according to job description.
Assign the percentage matching  based on job description and the missing keyworkds with high accuracy.
resume : {text}
description : {jd}

I want the response in one single string having a structure like -  
{{"JD Match" : "%", "MissingKeywords" : [], "Profile Summary" : ""}}
"""
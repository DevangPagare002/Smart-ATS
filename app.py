import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import PyPDF2 as pdf
import json

load_dotenv() ## Load my environment variables.

st.set_page_config(layout="wide")

genai.configure(api_key = os.getenv("GEM_API_KEY")) ## Configuring the API key
## Below function gets the response from gemini-pro
def get_gemini_response(input):
    model = genai.GenerativeModel("gemini-pro") ## Calling Gemini model
    response = model.generate_content(input)
    return response.text

## Below function reads text from pdf
def read_text_from_pdf(uploaded_files):
    reader = pdf.PdfReader(uploaded_files) ## Read the pdf
    text = ""
    for page in range(len(reader.pages)): ## Loop over each page
        page = reader.pages[page]
        text += str(page.extract_text()) ## Append page-text into text variable

    return text


## Streamlit app
st.title("Smart ATS")

st.subheader("Improve your resume by ATS")
st.write("")

jd = st.text_area(r"$\textsf{\Large Paste the Job Description}$")

uploaded_files = st.file_uploader(r"$\textsf{\Large Upload your resume}$", type="pdf", help="Please upload the resume in pdf format")

if uploaded_files:
    text = read_text_from_pdf(uploaded_files)
    
    ## Input prompt
    input_prompt = f"""
    Hii, Act like you are a very skillful or experienced ATS(Application Tracking System).
    You have deep understanding of tech field, software engineering, data science, data analysis and big data
    engineer. Your task is to evaluate the resume based on given job description.
    You must consider that the job market is very competitive and you should provide bjest assistance for improving the resume according to job description.
    Assign the percentage matching  based on job description and the missing keyworkds with high accuracy. \n
    __resume__ : {text}\n
    __description__ : {jd}

    I want the response in one single string having a json structure like -  
    {{"Job description Match" : "%", 
     "Missing Keywords from resume" : "[]", 
     "job description Summary" : "", 
     "Resume summary" : "",
     "Is candidate fit for job" : "yes/no"}}
    """

if not uploaded_files:
    st.error("Please upload the resume.")
    st.stop()
if not jd:
    st.error("Please paste the job description.")
    st.stop()


submit = st.button("Submit")

if submit:
    if uploaded_files is not None:
        text = read_text_from_pdf(uploaded_files)
        response = get_gemini_response(input_prompt)
        dict_start = response.index("{")
        dict_end = response.index("}")
        complete_dict = response[dict_start:dict_end + 1]
        dictionary = json.loads(complete_dict)
        st.write(dictionary)
        st.subheader("Dump text")
        st.write(response)
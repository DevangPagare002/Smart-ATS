import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
from pathlib import Path


# load_dotenv() ## Load my environment variables.
llama-parser-api = st.secrets["api keys"]["LLAMA_CLOUD_API_KEY"]

st.set_page_config(layout="wide")

## Below function gets the response from gemini-pro
def get_gemini_response(input):
    model = genai.GenerativeModel("gemini-pro") ## Calling Gemini model
    response = model.generate_content(input)
    return response.text
    
def llama_parser(resume_path):
    parser = LlamaParse(
        result_type="markdown"  # "markdown" and "text" are available
    ).load_data(resume_path)

    # print(parser[0].text)

    return parser[0].text

# Custom CSS to align the title
st.markdown(
    """
    <style>
    .title {
        text-align: center;
    }

    .subheader {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit app with custom CSS class for the title
st.markdown('<h1 class="title">Smart ATS</h1>', unsafe_allow_html=True)

st.markdown('<h3 class="subheader">Improve your chances of getting call for the interview</h3>', unsafe_allow_html=True)
st.write("")

st.markdown("""
            * Compare your resume with the job description.
            * Know if you are the right fit for the job.
            * Get the key points to improve in your resume.
            #### Enter your Gemini API key below. If you don't have any, create one for free by clicking [here](https://aistudio.google.com/app/apikey)""")
api = st.text_input("", label_visibility="collapsed")

if api:
    genai.configure(api_key = api) ## Configuring the API key

uploaded_files = st.file_uploader(r"$\textsf{\Large Upload your resume}$", type="pdf", help="Please upload the resume in pdf format")

jd = st.text_area(r"$\textsf{\Large Paste the Job Description}$")

if uploaded_files:

    save_folder = "resumes"
    save_path = Path(save_folder, uploaded_files.name)
    with open(save_path, mode='wb') as w:
        w.write(uploaded_files.getvalue())
    
    if save_path.exists():
        st.success(f'File {uploaded_files.name} is successfully saved!')

    text = llama_parser(f"./resumes/{uploaded_files.name}")

    # st.write(text)

    input_prompt = f"""
You are a very skillful and experienced ATS(Application Tracking System).
You have deep understanding of tech field, software engineering, data science, data analysis and big data engineering. The candidate we are about to hire is going to complete a very important project which is very essential for the organization, so you must review the candidate carefully.
Your task is to evaluate the resume based on given job description. For this, the standard ATS behaviour you should follow is - 

1. First, check if the experience required in job description is greater than the candidate experience.
2. Check what are the required technical and non-technical skills for the job.
3. Check if the resume contains those technical skills or not.
4. Do not do the word to word check, instead use your intuition to check if the candidate of this resume will be able to do the job or not.
5. Keep in mind that resume or job description might use short forms or synonyms for some keywords. eg. "Project manager" can be written as PM in JD, but it is mentioned as "project manager" in resume. Then you have to be aware enough to not flag it as missing word.


Assign the percentage matching  based on job description and the missing keywords with high accuracy. Below is the job description and resume. \n
__Job Description__ : {jd}
__Resume__ : {text}\n
Give response in one single string having a json structure like -  
{{"Job description Match with resume" : "%", 
 "Missing Keywords from resume" : "[mention the technologies that should be present in the resume to get higher match in comma seperated format]", 
 "job description Summary" : "", 
 "Resume summary" : "",
 "Is candidate fit for job" : "yes/no",
 "Reason for it" : ""}}
"""
    # st.write(input_prompt)

    if not uploaded_files:
        st.error("Please upload the resume.")
        st.stop()
    if not jd:
        st.error("Please paste the job description.")
        st.stop()

submit = st.button("Submit")

if submit:
    if uploaded_files is not None:
        # text = text_reader(uploaded_files.name)
        # st.markdown(text, unsafe_allow_html=True)
        # print(text)

        print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print(input_prompt)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
        response = get_gemini_response(input_prompt)
        print(response)
        dict_start = response.index("{")
        dict_end = response.index("}")
        complete_dict = response[dict_start:dict_end + 1]
        dictionary = json.loads(complete_dict)
        # st.write(dictionary)
        # print(dictionary)
        st.markdown(f"""#### Job description Match with resume : 
                    {dictionary['Job description Match with resume']}""")
        st.markdown(f"""#### Keywords that are missing in resume : 
                    {dictionary['Missing Keywords from resume']}""")
        st.markdown(f"""#### A summary of Job Description :
                     {dictionary['job description Summary']}""")
        st.markdown(f"""#### Your Resume summary : 
                    {dictionary['Resume summary']}""")
        st.markdown(f"""#### Are you fit for the job : 
                    {dictionary['Is candidate fit for job']}""")
        st.markdown(f"""#### Overall evaluation :
                    {dictionary['Reason for it']}""")
        # st.subheader("Dump text")
        # st.write(response)
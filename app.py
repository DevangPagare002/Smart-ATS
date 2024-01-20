import streamlit
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv() ## Load my environment variables.

genai.configure(api_key = os.getenv("GOOGLE_API_KEY")) ## Configuring the API key

def get_gemini_response(input):
    model = genai.GenerativeModel("gemini-pro") ## Calling Gemini model
    response = model.generate_content(input)
    response = json.loads(response.text)
    return response
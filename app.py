import streamlit
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv() ## Load my environment variables.

genai.configure(api_key = os.getenv("GOOGLE_API_KEY")) ## Configuring the API key

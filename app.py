import os

import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

prompt_template = """
You are an expert at planning oversea trips.

Please take the users request and plan a comprehensive trip for them.

Please include the following details:
- The destination
- The duration of the trip
- The activities that will be done
- The accommodation

The user's request is:
{prompt}
"""

def generate_content(prompt):
    response = model.generate_content(prompt)
    return response.text

st.title("🏝️ AI Travel Planning")

prompt = st.text_area("Enter your next travel request (days, destination, activities, etc.):")
if st.button("Give me a plan!"):
    reply = generate_content(prompt)
    st.write(reply)
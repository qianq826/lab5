import os

import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

def generate_content(prompt):
    response = model.generate_content(prompt)
    return response.text

prompt_template = """
You are an expert at planning overseas trips.

Please take the users request and plan a comprehensive trip for them.

Please include the following details:
- The destination
- The duration of the trip
- The dates of travel
- The flight options
- The activities that will be done
- The accommodation options

The user's request is:
{prompt}
"""

st.title("🏝️ AI Travel Planning")

# User input for travel details
destination = st.text_input("Destination:")
travel_dates = st.date_input("Travel dates:")
activities = st.text_area("Activities you're interested in:")
accommodation_preference = st.selectbox("Accommodation Preference:", ["Hotel", "Hostel", "Apartment", "Other"])

# Concatenating user inputs into a full request
full_request = f"Destination: {destination}, Dates: {travel_dates}, Activities: {activities}, Accommodation: {accommodation_preference}"

if st.button("Give me a plan!"):
    prompt = prompt_template.format(prompt=full_request)
    reply = generate_content(prompt)
    st.write(reply)


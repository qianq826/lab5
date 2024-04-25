import os
import psycopg2
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

# Configure API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# Database connection
def connect_db():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

# Insert trip to the database
def insert_trip(destination, departure_date, return_date, activities, accommodation, plan_details):
    conn = connect_db()
    cur = conn.cursor()
    sql = """INSERT INTO trips (destination, departure_date, return_date, activities, accommodation, plan_details)
             VALUES (%s, %s, %s, %s, %s, %s);"""
    cur.execute(sql, (destination, departure_date, return_date, activities, accommodation, plan_details))
    conn.commit()
    cur.close()
    conn.close()

# Generate content using Gemini API
def generate_content(prompt):
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI for trip planning
st.title("🏝️ AI Travel Planning")

prompt_template = """
You are an expert at planning overseas trips.

Please take the users request and plan a comprehensive trip for them.

Please include the following details:
- The destination
- The duration of the trip
- The departure and return dates
- The flight options
- The activities that will be done
- The accommodation options

The user's request is:
{prompt}
"""

# User inputs
destination = st.text_input("Destination")
departure_date = st.date_input("Departure Date")
return_date = st.date_input("Return Date")
activities = st.text_area("Activities you're interested in")
accommodation_preference = st.selectbox("Accommodation Preference", ["Hotel", "Hostel", "Apartment", "Other"])

if st.button("Give me a plan!"):
    full_request = f"Destination: {destination}, Departure Date: {departure_date}, Return Date: {return_date}, Activities: {activities}, Accommodation: {accommodation_preference}"
    prompt = prompt_template.format(prompt=full_request)
    reply = generate_content(prompt)
    st.write(reply)
    # Save to database
    insert_trip(destination, departure_date, return_date, activities, accommodation_preference, reply)
    st.success("Trip saved successfully!")

# Display saved trips from the database
if st.checkbox("Show Saved Trips"):
    st.header("Saved Trips")
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM trips")
    trips = cur.fetchall()
    cur.close()
    conn.close()
    if trips:
        for trip in trips:
            st.subheader(f"Trip to {trip[1]}")
            st.text(f"Dates: {trip[2]} to {trip[3]}")
            st.text(f"Activities: {trip[4]}")
            st.text(f"Accommodation: {trip[5]}")
            st.text(f"Plan Details: {trip[6]}")
    else:
        st.error("No saved trips found.")

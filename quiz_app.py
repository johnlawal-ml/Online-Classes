import streamlit as st
import pandas as pd
import os
import time

# Path to the results file
results_file = "quiz_results.csv"
total_time = 20 * 60  # 20 minutes in seconds

# Function to save student details and scores
def save_results(student_name, student_id, score):
    if not os.path.exists(results_file):
        # Create the file with headers if it doesn't exist
        with open(results_file, "w") as f:
            f.write("Name,Student ID,Score\n")

    # Append the student's details and score to the file
    with open(results_file, "a") as f:
        f.write(f"{student_name},{student_id},{score}\n")

# Function to load existing student data
def load_existing_data():
    if os.path.exists(results_file):
        return pd.read_csv(results_file)
    else:
        return pd.DataFrame(columns=["Name", "Student ID", "Score"])

# Display the logo at the top
st.image("logo.png", width=100)  # Adjust width as needed

# Title of the quiz
st.title('Class Quiz')

# Initialize session state variables
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'student_responses' not in st.session_state:
    st.session_state.student_responses = {}

# Sidebar for student details
st.sidebar.title("Student Details")
student_name = st.sidebar.text_input("Name")
student_id = st.sidebar.text_input("Student ID")

# Load existing student data to check for duplicates
existing_data = load_existing_data()

if student_id in existing_data["Student ID"].values:
    st.sidebar.warning("You have already submitted your answers. Thank you!")
else:
    # Define the questions and choices
    questions = [
        {
            "question": "What is the capital of France?",
            "options": ["Berlin", "Madrid", "Paris", "Rome"],
            "answer": "Paris"
        },
        {
            "question": "What is 2 + 2?",
            "options": ["3", "4", "5", "6"],
            "answer": "4"
        },
        {
            "question": "Who wrote 'To Kill a Mockingbird'?",
            "options": ["Harpe

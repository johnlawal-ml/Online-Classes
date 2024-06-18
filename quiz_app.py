import streamlit as st
import pandas as pd
import os

# Path to the results file
results_file = "quiz_results.csv"

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

# Sidebar for student details
st.sidebar.title("Student Details")
student_name = st.sidebar.text_input("Name")
student_id = st.sidebar.text_input("Student ID")

# Load existing student data to check for duplicates
existing_data = load_existing_data()

if student_id in existing_data["Student ID"].values:
    st.sidebar.warning("You have already submitted your answers. Thank you!")
else:
    # Introduction text
    st.write("""
    Welcome to the class quiz! Please answer the following questions:
    """)

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
            "options": ["Harper Lee", "J.K. Rowling", "Mark Twain", "Ernest Hemingway"],
            "answer": "Harper Lee"
        }
    ]

    # Store student responses
    student_responses = {}

    # Display each question
    for i, q in enumerate(questions):
        st.write(f"**Question {i + 1}:** {q['question']}")
        student_responses[i] = st.radio(f"Select your answer for Question {i + 1}:", q['options'])

    # Submit button
    if st.button('Submit'):
        if not student_name or not student_id:
            st.error("Please fill in both your name and student ID.")
        else:
            correct_answers = 0
            total_questions = len(questions)

            for i, q in enumerate(questions):
                if student_responses[i] == q['answer']:
                    correct_answers += 1

            # Save student details and score
            save_results(student_name, student_id, correct_answers)

            # Display results
            st.write(f"You answered {correct_answers} out of {total_questions} questions correctly.")

            # Feedback message
            if correct_answers == total_questions:
                st.success("Excellent! You got all questions right!")
            elif correct_answers >= total_questions / 2:
                st.info("Good job! You got more than half of the questions right.")
            else:
                st.warning("You need more practice. Better luck next time!")

            st.sidebar.success("Details submitted successfully!")

# Admin section to download results
st.sidebar.title("Admin Section")
if st.sidebar.checkbox('Show download link for results'):
    if os.path.exists(results_file):
        with open(results_file, 'rb') as f:
            st.sidebar.download_button(
                label='Download Results',
                data=f,
                file_name=results_file,
                mime='text/csv'
            )
    else:
        st.sidebar.write("No results available yet.")

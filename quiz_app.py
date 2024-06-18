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
            "options": ["Harper Lee", "J.K. Rowling", "Mark Twain", "Ernest Hemingway"],
            "answer": "Harper Lee"
        }
    ]

    # Timer
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = total_time - elapsed_time

    if remaining_time <= 0:
        st.warning("Time is up! Submitting your answers...")
        submit_quiz = True
    else:
        st.sidebar.write(f"Time remaining: {int(remaining_time // 60)} minutes {int(remaining_time % 60)} seconds")
        submit_quiz = False

    # Display the current question
    current_question = st.session_state.current_question
    question = questions[current_question]

    st.write(f"**Question {current_question + 1}:** {question['question']}")
    st.session_state.student_responses[current_question] = st.radio(
        "Select your answer:", question["options"], key=current_question
    )

    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])

    if current_question > 0:
        if col1.button("Previous"):
            st.session_state.current_question -= 1

    if current_question < len(questions) - 1:
        if col3.button("Next"):
            st.session_state.current_question += 1
    else:
        submit_quiz = col3.button("Submit")

    # Submit quiz
    if submit_quiz:
        if not student_name or not student_id:
            st.error("Please fill in both your name and student ID.")
        else:
            correct_answers = 0
            total_questions = len(questions)

            for i, q in enumerate(questions):
                if st.session_state.student_responses.get(i) == q["answer"]:
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
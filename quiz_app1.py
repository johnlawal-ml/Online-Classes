import streamlit as st
import pandas as pd
import os
import time

# Define the questions and choices (using a reduced set of questions for clarity)
questions = [
    {
        "question": "Which of the following is the correct formula to add cells A1 and B1 in Excel?",
        "options": ["=A1+B1", "=SUM(A1:B1)", "=ADD(A1, B1)", "=A1-B1"],
        "answer": "=A1+B1"
    },
    {
        "question": "What function would you use to calculate the average of a range of cells in Excel?",
        "options": ["=MEAN()", "=AVG()", "=AVERAGE()", "=SUM()/COUNT()"],
        "answer": "=AVERAGE()"
    },
    {
        "question": "Which of the following is not a logical operator in Excel?",
        "options": ["AND", "OR", "NOT", "IF"],
        "answer": "IF"
    }
]

# Path to the results file
results_file = "quiz_results.csv"
total_time = 20 * 60  # 20 minutes in seconds

# Function to save student details and scores
def save_results(student_name, student_email, score):
    if not os.path.exists(results_file):
        # Create the file with headers if it doesn't exist
        with open(results_file, "w") as f:
            f.write("Name,Email,Score\n")

    # Append the student's details and score to the file
    with open(results_file, "a") as f:
        f.write(f"{student_name},{student_email},{score}\n")

# Function to load existing student data
def load_existing_data():
    if os.path.exists(results_file):
        return pd.read_csv(results_file)
    else:
        return pd.DataFrame(columns=["Name", "Email", "Score"])

# Display the logo at the top
st.image("logo.png", width=100)  # Adjust width as needed

# Title of the quiz
st.title("Class Quiz")

# Initialize session state variables
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()

if 'student_responses' not in st.session_state:
    st.session_state.student_responses = {}

if 'current_question' not in st.session_state:
    st.session_state.current_question = 0

# Sidebar for student details
st.sidebar.title("Student Details")
student_name = st.sidebar.text_input("Name")
student_email = st.sidebar.text_input("Email")

# Load existing student data to check for duplicates
existing_data = load_existing_data()

if student_email in existing_data["Email"].values:
    st.sidebar.warning("You have already submitted your answers. Thank you!")
elif student_name and student_email:
    if not st.session_state.submitted:
        # Calculate the remaining time
        remaining_time = total_time - (time.time() - st.session_state.start_time)
        
        if remaining_time < 0:
            remaining_time = 0
        
        # Display the countdown timer using JavaScript
        st.markdown(f"""
        <script>
        function startTimer(duration, display) {{
            var timer = duration, minutes, seconds;
            setInterval(function () {{
                minutes = parseInt(timer / 60, 10);
                seconds = parseInt(timer % 60, 10);

                minutes = minutes < 10 ? "0" + minutes : minutes;
                seconds = seconds < 10 ? "0" + seconds : seconds;

                display.textContent = "Time remaining: " + minutes + ":" + seconds;

                if (--timer < 0) {{
                    timer = 0;
                    document.getElementById("submit-button").click(); // Automatically submit when time is up
                }}
            }}, 1000);
        }}

        window.onload = function () {{
            var totalSeconds = {int(remaining_time)},
                display = document.querySelector('#time');
            startTimer(totalSeconds, display);
        }};
        </script>
        <div id="time" style="font-size: 20px;"></div>
        """, unsafe_allow_html=True)
        
        # Display all questions on a single page
        for i, question in enumerate(questions):
            st.markdown(f"**Question {i + 1}:** {question['question']}")
            st.session_state.student_responses[i] = st.radio(
                f"Select your answer for Question {i + 1}:", question["options"], key=i
            )
            st.write("")  # Add space between questions

        # Submit button
        if st.button("Submit", key="submit-button"):
            st.session_state.submitted = True

            # Submit quiz
            if not student_name or not student_email:
                st.error("Please fill in both your name and email.")
            else:
                correct_answers = 0
                total_questions = len(questions)

                for i, q in enumerate(questions):
                    if st.session_state.student_responses[i] == q["answer"]:
                        correct_answers += 1

                # Save student details and score
                save_results(student_name, student_email, correct_answers)

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

else:
    st.sidebar.warning("Please enter your name and email to start the quiz.")

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

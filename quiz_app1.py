import streamlit as st
import pandas as pd
import os
import time

# Define the questions and choices
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

# Function to format time
def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{int(minutes)}:{int(seconds):02d}"

# Display the logo at the top
st.image("logo.png", width=100)  # Adjust width as needed

# Title of the quiz with timer on the right
st.markdown(
    """
    <style>
        #timer {
            font-size: 24px;
            background-color: white;
            padding: 10px;
            border: 1px solid black;
            border-radius: 10px;
            position: absolute;
            right: 20px;
        }
    </style>
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <h1>Class Quiz</h1>
        <div id="timer">Time remaining: </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar for student details
st.sidebar.title("Student Details")
student_name = st.sidebar.text_input("Name")
student_email = st.sidebar.text_input("Email")

# Initialize session state variables
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'student_responses' not in st.session_state:
    st.session_state.student_responses = {}
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# Load existing student data to check for duplicates
existing_data = load_existing_data()

if student_email in existing_data["Email"].values:
    st.sidebar.warning("You have already submitted your answers. Thank you!")
elif student_name and student_email:
    if st.session_state.start_time is None:
        st.session_state.start_time = time.time()
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = total_time - elapsed_time

    if remaining_time <= 0:
        st.session_state.submitted = True
        remaining_time = 0
    else:
        # Display the countdown timer
        st.markdown(
            f"""
            <script>
                function updateTimer() {{
                    var timerElement = document.getElementById("timer");
                    var remainingTime = {remaining_time};
                    var timerInterval = setInterval(function() {{
                        var minutes = Math.floor(remainingTime / 60);
                        var seconds = remainingTime % 60;
                        timerElement.innerHTML = "Time remaining: " + minutes + ":" + (seconds < 10 ? "0" : "") + seconds;
                        remainingTime--;
                        if (remainingTime < 0) {{
                            clearInterval(timerInterval);
                            window.location.reload();  // Reload page after time is up
                        }}
                    }}, 1000);
                }}
                updateTimer();
            </script>
            """,
            unsafe_allow_html=True
        )

    # Display the current question
    current_question = st.session_state.current_question
    question = questions[current_question]
    st.markdown(f"**Question {current_question + 1}:** {question['question']}")
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
        if col3.button("Submit"):
            submit_quiz = True

    # Submit quiz
    if 'submit_quiz' in locals():
        if not student_name or not student_email:
            st.error("Please fill in both your name and email.")
        else:
            correct_answers = 0
            total_questions = len(questions)

            for i, q in enumerate(questions):
                if st.session_state.student_responses.get(i) == q["answer"]:
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

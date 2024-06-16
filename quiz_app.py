import streamlit as st

# Title of the quiz
st.title('TechNTransit Excel Class Exercise')

# Introduction text
st.write("""
Welcome to the TechNTransit Excel Class Exercise! Please answer the following questions:
""")

# Define the questions and choices
questions = [
    {
        "question": "Which of the following is the correct formula to add cells A1 and B1 in Excel?",
        "options": ["=A1+B1", "=SUM(A1`:`B1)", "=ADD(A1, B1)", "=A1-B1"],
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
    },
    {
        "question": "What will be the result of the formula =AND(TRUE, FALSE)?",
        "options": ["TRUE", "FALSE", "ERROR", "#VALUE!"],
        "answer": "FALSE"
    },
    {
        "question": "Which function calculates the total sum of a range in Excel?",
        "options": ["=SUM()", "=TOTAL()", "=ADD()", "=COUNT()"],
        "answer": "=SUM()"
    },
    {
        "question": "To find the smallest number in a range of cells, which function should you use?",
        "options": ["=MINIMUM()", "=LOW()", "=MIN()", "=LEAST()"],
        "answer": "=MIN()"
    },
    {
        "question": "Which of the following can you do with Conditional Formatting in Excel?",
        "options": ["Change cell values", "Format cells based on criteria", "Create Pivot Tables", "Apply data validation"],
        "answer": "Format cells based on criteria"
    },
    {
        "question": "How would you apply a color scale to a range of cells based on their values in Excel?",
        "options": ["Use the Color function", "Use Data Validation", "Use Conditional Formatting", "Use the Find and Replace tool"],
        "answer": "Use Conditional Formatting"
    },
    {
        "question": "Which function is used to search for a value in the first column of a table and return a value in the same row from a specified column?",
        "options": ["VLOOKUP", "HLOOKUP", "LOOKUP", "SEARCH"],
        "answer": "VLOOKUP"
    },
    {
        "question": "What does the FALSE parameter in the VLOOKUP function signify?",
        "options": ["Approximate match", "Exact match", "Case-insensitive match", "Case-sensitive match"],
        "answer": "Exact match"
    },
    {
        "question": "What can you use Data Validation for in Excel?",
        "options": ["To restrict the type of data that can be entered in a cell", "To perform complex calculations", "To format cells based on criteria", "To create charts and graphs"],
        "answer": "To restrict the type of data that can be entered in a cell"
    },
    {
        "question": "Which Data Validation criteria would you use to ensure a cell only accepts dates?",
        "options": ["Text Length", "List", "Date", "Custom"],
        "answer": "Date"
    },
    {
        "question": "Which of the following is true about Pivot Tables in Excel?",
        "options": ["They are used to summarize and analyze data", "They automatically update when the source data changes", "They are a type of chart", "They require complex formulas to create"],
        "answer": "They are used to summarize and analyze data"
    },
    {
        "question": "How can you refresh a Pivot Table to reflect changes in the source data?",
        "options": ["Right-click the Pivot Table and select Refresh", "Double-click any cell in the Pivot Table", "Click Insert and then Refresh", "Delete the Pivot Table and create a new one"],
        "answer": "Right-click the Pivot Table and select Refresh"
    },
    {
        "question": "Which function counts the number of cells that contain numbers in a range?",
        "options": ["=COUNT()", "=COUNTA()", "COUNTIF()", "COUNTBLANK()"],
        "answer": "=COUNT()"
    },
    {
        "question": "Which logical function returns TRUE if any of its arguments are TRUE?",
        "options": ["OR", "AND", "NOT", "IF"],
        "answer": "OR"
    },
    {
        "question": "To find the largest number in a range of cells, which function should you use?",
        "options": ["=MAXIMUM()", "=HIGH()", "=MAX()", "=MOST()"],
        "answer": "=MAX()"
    },
    {
        "question": "What is the shortcut to create a new Pivot Table in Excel?",
        "options": ["Ctrl + N", "Alt + P", "Alt + N + V", "Ctrl + T"],
        "answer": "Alt + N + V"
    },
    {
        "question": "How can you highlight cells in Excel that are greater than a specific value?",
        "options": ["Use Data Validation", "Use Find and Replace", "Use Conditional Formatting", "Use Text to Columns"],
        "answer": "Use Conditional Formatting"
    },
    {
        "question": "What function would you use to look up a value in a row and return a value from the same column?",
        "options": ["VLOOKUP", "HLOOKUP", "LOOKUP", "SEARCH"],
        "answer": "HLOOKUP"
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
    correct_answers = 0
    total_questions = len(questions)

    for i, q in enumerate(questions):
        if student_responses[i] == q['answer']:
            correct_answers += 1

    # Display results
    st.write(f"You answered {correct_answers} out of {total_questions} questions correctly.")

    # Feedback message
    if correct_answers == total_questions:
        st.success("Excellent! You got all questions right!")
    elif correct_answers >= total_questions / 2:
        st.info("Good job! You got more than half of the questions right.")
    else:
        st.warning("You need more practice. Better luck next time!")

# Collecting student details
st.sidebar.title("Student Details")
student_name = st.sidebar.text_input("Name")
student_email = st.sidebar.text_input("Student Email")

# Store the student's name and ID
if st.sidebar.button("Submit Details"):
    if student_name and student_email:
        st.sidebar.write(f"Student Name: {student_name}")
        st.sidebar.write(f"Student Email: {student_email}")
        st.sidebar.success("Details submitted successfully!")
    else:
        st.sidebar.error("Please fill in both your name and student Email.")

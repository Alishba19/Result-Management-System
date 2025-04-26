import streamlit as st
from datetime import datetime
import json
import os

# Constants 
DATA_FILE = "student_results.json"

# OOP Classes 
class Student:
    def __init__(self, name, roll_number):
        self.name = name
        self.roll_number = roll_number
        self.results = {}

    def add_result(self, subject, marks):
        self.results[subject] = marks

    def get_total_marks(self):
        return sum(self.results.values())

    def get_percentage(self):
        total_marks = self.get_total_marks()
        total_subjects = len(self.results)
        if total_subjects == 0:
            return 0
        return (total_marks / (total_subjects * 100)) * 100

    def get_grade(self):
        percentage = self.get_percentage()
        if percentage >= 90:
            return 'A+'
        elif percentage >= 80:
            return 'A'
        elif percentage >= 70:
            return 'B+'
        elif percentage >= 60:
            return 'B'
        elif percentage >= 50:
            return 'C'
        elif percentage >= 40:
            return 'D'
        else:
            return 'F'

class ResultSystem:
    def __init__(self):
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def get_all_students(self):
        return self.students

#  File Handling 
def save_data(result_system):
    data = [{
        "name": student.name,
        "roll_number": student.roll_number,
        "results": student.results
    } for student in result_system.students]
    
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def load_data(result_system):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            for item in data:
                student = Student(item["name"], item["roll_number"])
                for subject, marks in item["results"].items():
                    student.add_result(subject, marks)
                result_system.add_student(student)

#  Streamlit UI 
st.set_page_config(page_title="Result Management System", layout="centered")

if 'result_system' not in st.session_state:
    st.session_state.result_system = ResultSystem()
    load_data(st.session_state.result_system)

st.title("📚 Result Management System")

#  Add Student 
st.header("Add New Student")
with st.form("student_form"):
    name = st.text_input("Student Name")
    roll_number = st.text_input("Roll Number")

    submitted = st.form_submit_button("Add Student")
    if submitted and name and roll_number:
        student = Student(name, roll_number)
        st.session_state.result_system.add_student(student)
        save_data(st.session_state.result_system)
        st.success(f"Student {name} added successfully!")

#  Add Results
st.header("Add Results")
student_names = [student.name for student in st.session_state.result_system.get_all_students()]
selected_student_name = st.selectbox("Select Student", student_names)

# Check if there are students matching the selected name
matching_students = [student for student in st.session_state.result_system.get_all_students() if student.name == selected_student_name]

if matching_students:
    selected_student = matching_students[0]  # Get the first match (since names are unique)
    
    with st.form("result_form"):
        subject = st.text_input("Subject Name")
        marks = st.number_input("Marks Obtained", min_value=0, max_value=100)
        
        submitted_result = st.form_submit_button("Add Result")
        if submitted_result and subject and marks is not None:
            selected_student.add_result(subject, marks)
            save_data(st.session_state.result_system)
            st.success(f"Result for {subject} added successfully!")
else:
    st.warning(f"No student found with the name {selected_student_name}.")

# View All Students and Results 
st.header("All Students and Results")
for student in st.session_state.result_system.get_all_students():  # Fixed here
    st.write(f"**{student.name}** (Roll No: {student.roll_number})")
    st.write(f"Total Marks: {student.get_total_marks()} / {len(student.results)*100}")
    st.write(f"Percentage: {student.get_percentage():.2f}%")
    st.write(f"Grade: {student.get_grade()}")
    st.write("Results:")
    for subject, marks in student.results.items():
        st.write(f"  - {subject}: {marks} marks")

#  Student Search 
st.header("Search Student Results")
search_name = st.text_input("Enter Student Name to Search")
if search_name:
    matching_students = [student for student in st.session_state.result_system.get_all_students()  # Fixed here
                        if search_name.lower() in student.name.lower()]
    for student in matching_students:
        st.write(f"**{student.name}** (Roll No: {student.roll_number})")
        st.write(f"Total Marks: {student.get_total_marks()} / {len(student.results)*100}")
        st.write(f"Percentage: {student.get_percentage():.2f}%")
        st.write(f"Grade: {student.get_grade()}")
        st.write("Results:")
        for subject, marks in student.results.items():
            st.write(f"  - {subject}: {marks} marks")
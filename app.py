import streamlit as st
import sqlite3
from datetime import date

# --- DATABASE SETUP ---
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        class TEXT,
        school_name TEXT,
        parent_name TEXT,
        contact TEXT,
        registration_date TEXT
    )
''')
conn.commit()


# --- STUDENT REGISTRATION FUNCTION ---
def register_student():
    st.header("📋 Student Registration Form")

    name = st.text_input("Student Name")
    class_ = st.selectbox("Class", ['UKG', 'LKG'] + [str(i) for i in range(1, 11)])
    school_name = st.text_input("School Name")
    parent_name = st.text_input("Parent Name")
    contact = st.text_input("Contact Number")
    registration_date = st.date_input("Date of Registration", date.today())

    if st.button("Submit"):
        if name and class_ and school_name and parent_name and contact:
            cursor.execute('''
                INSERT INTO students (name, class, school_name, parent_name, contact, registration_date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, class_, school_name, parent_name, contact, str(registration_date)))
            conn.commit()
            st.success("✅ Student registered successfully!")
        else:
            st.error("❗ Please fill all the fields.")


# --- ADMIN VIEW FUNCTION ---
def admin_view():
    st.header("🔐 Admin Panel")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin123":  # Simple hardcoded login
            st.success("Welcome, Admin!")
            cursor.execute("SELECT * FROM students")
            data = cursor.fetchall()

            if data:
                st.subheader("📊 Registered Students")
                for row in data:
                    st.write(f"""
                    **ID:** {row[0]}  
                    **Name:** {row[1]}  
                    **Class:** {row[2]}  
                    **School:** {row[3]}  
                    **Parent:** {row[4]}  
                    **Contact:** {row[5]}  
                    **Date:** {row[6]}
                    """)
                    st.markdown("---")
            else:
                st.info("No registrations yet.")
        else:
            st.error("Invalid credentials")


# --- MAIN APP ---
st.set_page_config(page_title="Student Registration", layout="centered")

st.title("📚 Anjanikumar Tutorials Registration")

menu = st.sidebar.selectbox("Menu", ["Register", "Admin Login"])

if menu == "Register":
    register_student()
elif menu == "Admin Login":
    admin_view()

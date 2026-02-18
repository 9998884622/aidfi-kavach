import streamlit as st
import json
import os
from fpdf import FPDF


# ---------------- FILE PATH ----------------

USER_FILE = "users.json"

REPORT_FOLDER = "reports"

os.makedirs(REPORT_FOLDER, exist_ok=True)



# ---------------- LOAD USERS ----------------

def load_users():

    if os.path.exists(USER_FILE):

        with open(USER_FILE, "r") as f:

            return json.load(f)

    return {}



# ---------------- SAVE USERS ----------------

def save_users(users):

    with open(USER_FILE, "w") as f:

        json.dump(users, f)



# ---------------- FAKE ANALYSIS ----------------

def analyze(filename):

    return {

        "File Name": filename,
        "Failed Logins": 12,
        "Unauthorized Access": "Detected",
        "Risk Level": "HIGH",
        "AI Confidence": "98%"
    }



# ---------------- PDF ----------------

def create_pdf(report, user):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", size=12)


    for k, v in report.items():

        pdf.cell(200, 10, txt=f"{k}: {v}", ln=True)


    path = f"{REPORT_FOLDER}/{user}_report.pdf"

    pdf.output(path)

    return path




# ---------------- SESSION ----------------

if "page" not in st.session_state:

    st.session_state.page = "login"

if "user" not in st.session_state:

    st.session_state.user = None

if "report" not in st.session_state:

    st.session_state.report = None




users = load_users()



# =====================================================
# REGISTER PAGE
# =====================================================

if st.session_state.page == "register":


    st.title("Register")


    email = st.text_input("Email")

    password = st.text_input("Password", type="password")


    if st.button("Register"):


        if email == "" or password == "":

            st.error("* Fill all fields")


        elif email in users:

            st.error("* Email exists")


        else:

            users[email] = password

            save_users(users)

            st.success("Register Successfully")

            st.session_state.page = "login"

            st.rerun()



    if st.button("Go Login"):

        st.session_state.page = "login"

        st.rerun()




# =====================================================
# LOGIN PAGE
# =====================================================

elif st.session_state.page == "login":


    st.title("Login")


    email = st.text_input("Email")

    password = st.text_input("Password", type="password")


    if st.button("Login"):


        if email not in users:

            st.error("* Email not registered")


        elif users[email] != password:

            st.error("* Wrong password")


        else:

            st.session_state.user = email

            st.session_state.page = "admin"

            st.rerun()



    if st.button("Register"):

        st.session_state.page = "register"

        st.rerun()




# =====================================================
# ADMIN UPLOAD PAGE
# =====================================================

elif st.session_state.page == "admin":


    st.title("Admin Evidence Upload")


    st.write("Welcome:", st.session_state.user)


    file = st.file_uploader("Upload Evidence")


    if file:


        if st.button("Analyze"):


            report = analyze(file.name)


            st.session_state.report = report


            st.session_state.page = "output"

            st.rerun()



    if st.button("Logout"):

        st.session_state.user = None

        st.session_state.page = "login"

        st.rerun()




# =====================================================
# OUTPUT PAGE
# =====================================================

elif st.session_state.page == "output":


    st.title("Investigation Report")


    report = st.session_state.report


    for k, v in report.items():

        st.write(k, ":", v)



    pdf = create_pdf(report, st.session_state.user)


    st.download_button(

        "Download PDF",

        open(pdf, "rb"),

        file_name="report.pdf"

    )


    if st.button("Back to Admin"):

        st.session_state.page = "admin"

        st.rerun()

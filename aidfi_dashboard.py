import streamlit as st
import json
import os
import datetime
from fpdf import FPDF

# folders
USER_FILE = "users.json"
STORAGE_FOLDER = "storage"
REPORT_FOLDER = "reports"

# create folders if not exist
os.makedirs(STORAGE_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)


# load users
def load_users():

    if os.path.exists(USER_FILE):

        with open(USER_FILE, "r") as f:
            return json.load(f)

    return {}


# save users
def save_users(users):

    with open(USER_FILE, "w") as f:
        json.dump(users, f)



# fake AI analysis
def analyze_file(filename):

    report = {

        "Total Events": 15230,
        "Suspicious": 42,
        "Risk Level": "HIGH",
        "AI Confidence": "98%",
        "Analysis":

        f"""
        Multiple Failed Logins detected
        Unauthorized access attempt found
        File analyzed: {filename}
        """

    }

    return report



# generate PDF
def create_pdf(report, username):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", size=12)

    for key, value in report.items():

        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    filename = f"{REPORT_FOLDER}/{username}_report.pdf"

    pdf.output(filename)

    return filename




# UI THEME
st.set_page_config(page_title="AIDFI", layout="wide")

st.title("AIDFI – AI Digital Forensics Investigator")



menu = st.sidebar.selectbox(

"Select",

["Login", "Register"]

)



users = load_users()



# REGISTER
if menu == "Register":

    st.subheader("Register")

    email = st.text_input("Enter Gmail")

    password = st.text_input("Password", type="password")


    if st.button("Register"):

        if email in users:

            st.error("User exists")

        else:

            users[email] = password

            save_users(users)

            st.success("Registered Successfully")




# LOGIN
if menu == "Login":

    st.subheader("Login")

    email = st.text_input("Enter Gmail")

    password = st.text_input("Password", type="password")


    if st.button("Login"):

        if email in users and users[email] == password:

            st.success("Login Successful")

            st.session_state.user = email

        else:

            st.error("Invalid login")




# DASHBOARD
if "user" in st.session_state:

    st.subheader("Admin Dashboard")


    file = st.file_uploader(

    "Upload Evidence",

    type=None

    )


    if file:

        path = f"{STORAGE_FOLDER}/{file.name}"

        with open(path, "wb") as f:

            f.write(file.read())

        st.success("File uploaded")



        if st.button("Analyze Evidence"):

            report = analyze_file(file.name)

            st.write(report)



            save = st.radio(

            "Save report?",

            ["Yes", "No"]

            )


            if save == "Yes":

                pdf = create_pdf(report, email)

                st.success("Saved")

                st.download_button(

                "Download PDF",

                open(pdf, "rb"),

                file_name="report.pdf"

                )


            else:

                pdf = create_pdf(report, email)

                st.download_button(

                "Download Report",

                open(pdf, "rb"),

                file_name="report.pdf"

                )

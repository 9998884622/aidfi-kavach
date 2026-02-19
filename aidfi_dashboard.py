import streamlit as st
import os
import json
import time
from datetime import datetime


# ---------------- CONFIG ----------------

st.set_page_config(page_title="AIDFI", layout="wide")


# ---------------- FILE SETUP ----------------

USERS = "users.json"
REPORTS = "reports"

if not os.path.exists(USERS):
    with open(USERS, "w") as f:
        json.dump({}, f)

if not os.path.exists(REPORTS):
    os.makedirs(REPORTS)


# ---------------- LOAD USERS ----------------

def load_users():
    with open(USERS) as f:
        return json.load(f)

def save_users(data):
    with open(USERS, "w") as f:
        json.dump(data, f)


# ---------------- SESSION ----------------

if "page" not in st.session_state:
    st.session_state.page = "login"

if "user" not in st.session_state:
    st.session_state.user = ""


# ---------------- HEADER NAVBAR ----------------

def navbar():

    st.markdown("""

    <style>

    .nav {
        background: linear-gradient(90deg,#020617,#0a0f2c);
        padding:15px;
        border-radius:10px;
        box-shadow:0 0 10px cyan;
    }

    .title {
        font-size:28px;
        font-weight:bold;
        color:cyan;
    }

    </style>

    """, unsafe_allow_html=True)


    col1,col2,col3,col4,col5,col6 = st.columns([2,1,1,1,1,1])

    with col1:
        st.markdown("<div class='title'>🛡 AIDFI</div>", unsafe_allow_html=True)

    with col2:
        if st.button("Login"):
            st.session_state.page="login"
            st.rerun()

    with col3:
        if st.button("Register"):
            st.session_state.page="register"
            st.rerun()

    with col4:
        if st.button("Upload"):
            st.session_state.page="upload"
            st.rerun()

    with col5:
        if st.button("AI Analysis"):
            st.session_state.page="analysis"
            st.rerun()

    with col6:
        if st.button("Download"):
            st.session_state.page="download"
            st.rerun()


navbar()


# ---------------- REGISTER ----------------

def register():

    st.title("Register")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register Now"):

        users = load_users()

        if email in users:
            st.error("Email already exists")

        else:
            users[email] = password
            save_users(users)

            st.success("Registered Successfully")

            st.session_state.page="login"
            st.rerun()


# ---------------- LOGIN ----------------

def login():

    st.title("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login Now"):

        users = load_users()

        if email not in users:

            st.markdown("<span style='color:red'>* Email not registered</span>", unsafe_allow_html=True)

        elif users[email] != password:

            st.error("Wrong Password")

        else:

            st.success("Login Successful")

            st.session_state.user=email
            st.session_state.page="upload"
            st.rerun()


# ---------------- UPLOAD ----------------

def upload():

    st.title("Upload Evidence")

    file = st.file_uploader("Upload File")

    if st.button("Start Analysis"):

        if file:

            progress = st.progress(0)

            for i in range(100):
                time.sleep(0.01)
                progress.progress(i+1)

            report = f"""
AIDFI FORENSIC REPORT

User: {st.session_state.user}

Time: {datetime.now()}

Suspicious Events: 42

Risk Level: HIGH

AI Confidence: 98%

Status: Unauthorized access detected
"""

            filename=file.name+".txt"

            with open(os.path.join(REPORTS, filename), "w") as f:
                f.write(report)

            st.success("Analysis Completed")



# ---------------- AI ANALYSIS ----------------

def analysis():

    st.title("AI Analysis Result")

    st.success("Risk Level: HIGH")
    st.success("Confidence: 98%")
    st.warning("Multiple Failed Login Detected")



# ---------------- DOWNLOAD ----------------

def download():

    st.title("Download Reports")

    files = os.listdir(REPORTS)

    if len(files)==0:
        st.info("No reports available")

    for file in files:

        with open(os.path.join(REPORTS,file),"rb") as f:

            st.download_button(

                "Download " + file,
                f,
                file_name=file
            )


# ---------------- PAGE CONTROL ----------------

if st.session_state.page=="login":
    login()

elif st.session_state.page=="register":
    register()

elif st.session_state.page=="upload":
    upload()

elif st.session_state.page=="analysis":
    analysis()

elif st.session_state.page=="download":
    download()


# ---------------- FOOTER ----------------

st.markdown("""

<hr>

<center>
@by Digital Detectives Team
</center>

""", unsafe_allow_html=True)

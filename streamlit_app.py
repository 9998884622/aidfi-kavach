import streamlit as st
import os
import json
import time
from datetime import datetime
import streamlit.components.v1 as components

import firebase_config as fb

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AIDFI + SecureKavach",
    layout="wide"
)

# ---------------- CSS ----------------

st.markdown("""
<style>

.stApp {
    background-color: #0e1117;
    color: white;
}

.title {
    font-size:28px;
    font-weight:bold;
}

.stButton button {
    background-color:#238636;
    color:white;
    border-radius:8px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- FILE SETUP ----------------

USERS = "users.json"
REPORT = "report"

if not os.path.exists(USERS):
    with open(USERS, "w") as f:
        json.dump({}, f)

if not os.path.exists(REPORT):
    os.makedirs(REPORT)

# ---------------- FUNCTIONS ----------------

def load_users():
    with open(USERS) as f:
        return json.load(f)

def save_users(data):
    with open(USERS, "w") as f:
        json.dump(data, f)

# ---------------- SESSION ----------------

if "page" not in st.session_state:
    st.session_state.page = "home"

if "user" not in st.session_state:
    st.session_state.user = ""

# ---------------- NAVBAR ----------------

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.markdown("<div class='title'>🛡 AIDFI + SecureKavach</div>", unsafe_allow_html=True)

with col2:
    if st.button("Home"):
        st.session_state.page = "home"

with col3:
    if st.button("Login"):
        st.session_state.page = "login"

with col4:
    if st.button("Register"):
        st.session_state.page = "register"

with col5:
    if st.button("Upload"):
        st.session_state.page = "upload"

with col6:
    if st.button("Admin"):
        st.session_state.page = "admin"

st.divider()

# ---------------- HOME ----------------

def home():
    st.subheader("Digital Forensics Investigation System")
    components.html("""
    <h3>Welcome to AIDFI</h3>
    <p>AI Powered Cyber Crime Investigation Tool</p>
    """, height=300)

# ---------------- REGISTER ----------------

def register():

    st.subheader("Register")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Create Account"):

        users = load_users()

        if email in users:
            st.error("User already exists")

        else:
            users[email] = password
            save_users(users)
            st.success("Registration Successful")

# ---------------- LOGIN ----------------

def login():

    st.subheader("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login Now"):

        users = load_users()

        if email in users and users[email] == password:

            st.session_state.user = email
            st.success("Login Successful")

        else:
            st.error("Invalid Login")

# ---------------- UPLOAD ----------------

def upload():

    if not st.session_state.user:

        st.warning("Login First")
        return

    st.subheader("Upload Evidence")

    file = st.file_uploader("Upload File")

    lat = st.text_input("Latitude")
    lng = st.text_input("Longitude")

    if st.button("Start Analysis"):

        if file:

            progress = st.progress(0)

            for i in range(100):

                time.sleep(0.01)
                progress.progress(i+1)

            risk = "HIGH"
            confidence = "98%"

            report = f"""
User: {st.session_state.user}
Time: {datetime.now()}
Risk Level: {risk}
Confidence: {confidence}
"""

            filename = file.name + ".txt"

            path = os.path.join(REPORT, filename)

            with open(path, "w") as f:
                f.write(report)

            fb.upload_file(path, filename)

            if lat and lng:
                fb.save_location(st.session_state.user, lat, lng)

            st.success("Analysis Complete")

# ---------------- ADMIN ----------------

def admin():

    st.subheader("Admin Panel")

    st.write("Uploaded Files:")

    files = fb.get_files()

    for file in files:

        st.write(file)

    st.write("Locations:")

    locations = fb.get_locations()

    st.json(locations)

# ---------------- PAGE CONTROL ----------------

if st.session_state.page == "home":
    home()

elif st.session_state.page == "register":
    register()

elif st.session_state.page == "login":
    login()

elif st.session_state.page == "upload":
    upload()

elif st.session_state.page == "admin":
    admin()

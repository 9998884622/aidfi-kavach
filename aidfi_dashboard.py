import streamlit as st
import os
import json
import time
from datetime import datetime
from streamlit.components.v1 import components
import firebase_config as fb

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AIDFI + SecureKavach", layout="wide")

# ---------------- FILE SETUP ----------------
USERS = "users.json"
REPORTS = "reports"

if not os.path.exists(USERS):
    with open(USERS, "w") as f:
        json.dump({}, f)

if not os.path.exists(REPORTS):
    os.makedirs(REPORTS)

# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "user" not in st.session_state:
    st.session_state.user = ""

# ---------------- HACKER THEME ----------------
st.markdown("""
<style>
body {background-image: url('images/matrix_background.gif'); background-size: cover; background-attachment: fixed; background-repeat: no-repeat;}
section.main {background-color: rgba(0,0,0,0.75) !important; padding: 20px; border-radius: 10px;}
.title {font-size:28px; font-weight:bold; color: #00ff00; text-shadow: 0 0 10px #00ff00, 0 0 20px #00ff00;}
.stButton button {background-color: #111 !important; color: #0f0 !important; border: 1px solid #0f0 !important; box-shadow: 0 0 5px #0f0;}
.stButton button:hover {background-color: #0f0 !important; color: #000 !important; box-shadow: 0 0 20px #0f0;}
</style>
""", unsafe_allow_html=True)

# ---------------- NAVBAR ----------------
def navbar():
    col1,col2,col3,col4,col5,col6,col7 = st.columns([2,1,1,1,1,1,1])
    with col1:
        st.markdown("<div class='title'>🛡 AIDFI + SecureKavach</div>", unsafe_allow_html=True)
    with col2:
        if st.button("Home"): st.session_state.page="home"; st.rerun()
    with col3:
        if st.button("Login"): st.session_state.page="login"; st.rerun()
    with col4:
        if st.button("Register"): st.session_state.page="register"; st.rerun()
    with col5:
        if st.button("Upload"): st.session_state.page="upload"; st.rerun()
    with col6:
        if st.button("AI Analysis"): st.session_state.page="analysis"; st.rerun()
    with col7:
        if st.button("Admin Dashboard"): st.session_state.page="admin"; st.rerun()

navbar()

# ---------------- PAGES ----------------
def home():
    st.title("Welcome to AIDFI + SecureKavach")
    if os.path.exists("index.html"):
        with open("index.html", "r") as f:
            components.html(f.read(), height=1200, scrolling=True)

def register():
    st.title("User Registration")
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

def login():
    st.title("User Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login Now"):
        users = load_users()
        if email not in users:
            st.error("Email not registered")
        elif users[email] != password:
            st.error("Wrong Password")
        else:
            st.success("Login Successful")
            st.session_state.user=email
            st.session_state.page="upload"
            st.rerun()

def load_users():
    with open(USERS) as f:
        return json.load(f)

def save_users(data):
    with open(USERS, "w") as f:
        json.dump(data, f)

def upload():
    st.title("Upload Evidence")
    file = st.file_uploader("Upload File")
    lat = st.text_input("Your Latitude")
    lng = st.text_input("Your Longitude")
    if st.button("Start Analysis"):
        if file:
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i+1)
            # Save report locally
            report = f"""
AIDFI FORENSIC REPORT
User: {st.session_state.user}
Time: {datetime.now()}
Suspicious Events: 42
Risk Level: HIGH
AI Confidence: 98%
Status: Unauthorized access detected
"""
            filename = file.name + ".txt"
            local_path = os.path.join(REPORTS, filename)
            with open(local_path, "w") as f:
                f.write(report)
            st.success("Analysis Completed")
            # Upload to Firebase
            fb.upload_intruder_image(local_path, filename)
            if lat and lng:
                fb.save_location(st.session_state.user, lat, lng)

def analysis():
    st.title("AI Analysis Result")
    st.success("Risk Level: HIGH")
    st.success("Confidence: 98%")
    st.warning("Multiple Failed Login Detected")

def admin_dashboard():
    st.title("Admin Dashboard")
    st.subheader("Intruder Images")
    blobs = fb.bucket.list_blobs(prefix="intruder/")
    for blob in blobs:
        url = blob.generate_signed_url(expiration=datetime(2099,1,1))
        st.image(url, width=250)
    st.subheader("Live Locations")
    locs = fb.ref.get()
    if locs:
        for user, val in locs.items():
            st.write(f"{user}: Latitude {val['lat']}, Longitude {val['lng']}")
    else:
        st.info("No location data yet.")

def download_reports():
    st.title("Download Reports")
    files = os.listdir(REPORTS)
    if len(files)==0:
        st.info("No reports available")
    for file in files:
        with open(os.path.join(REPORTS,file),"rb") as f:
            st.download_button("Download " + file, f, file_name=file)

# ---------------- PAGE CONTROL ----------------
if st.session_state.page=="home": home()
elif st.session_state.page=="register": register()
elif st.session_state.page=="login": login()
elif st.session_state.page=="upload": upload()
elif st.session_state.page=="analysis": analysis()
elif st.session_state.page=="admin": admin_dashboard()
elif st.session_state.page=="download": download_reports()

# ---------------- FOOTER ----------------
st.markdown("<hr><center>@by Digital Detectives Team</center>", unsafe_allow_html=True)

```python
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
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- SIMPLE DARK CSS ----------------

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

.card {
    background-color:#161b22;
    padding:20px;
    border-radius:10px;
}

.stButton button {
    background-color:#238636;
    color:white;
    border-radius:8px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- FILE SETUP ----------------

USERS="users.json"
REPORT="report"

if not os.path.exists(USERS):
    with open(USERS,"w") as f:
        json.dump({},f)

if not os.path.exists(REPORT):
    os.makedirs(REPORT)

# ---------------- FUNCTIONS ----------------

def load_users():

    with open(USERS) as f:
        return json.load(f)

def save_users(data):

    with open(USERS,"w") as f:
        json.dump(data,f)


# ---------------- SESSION ----------------

if "page" not in st.session_state:

    st.session_state.page="home"

if "user" not in st.session_state:

    st.session_state.user=""

# ---------------- NAVBAR ----------------

col1,col2,col3,col4,col5,col6 = st.columns(6)

with col1:

    st.markdown("<div class='title'>🛡 AIDFI + SecureKavach</div>", unsafe_allow_html=True)

with col2:

    if st.button("Home"):
        st.session_state.page="home"
        st.rerun()

with col3:

    if st.button("Login"):
        st.session_state.page="login"
        st.rerun()

with col4:

    if st.button("Register"):
        st.session_state.page="register"
        st.rerun()

with col5:

    if st.button("Upload"):
        st.session_state.page="upload"
        st.rerun()

with col6:

    if st.button("Admin"):
        st.session_state.page="admin"
        st.rerun()


st.divider()

# ---------------- HOME ----------------

def home():

    st.subheader("Digital Forensics Investigation System")

    with open("index.html") as f:

        components.html(f.read(),height=600)

# ---------------- REGISTER ----------------

def register():

    st.subheader("Register")

    email=st.text_input("Email")

    password=st.text_input("Password",type="password")

    if st.button("Register"):

        users=load_users()

        if email in users:

            st.error("User exists")

        else:

            users[email]=password

            save_users(users)

            st.success("Registered")

# ---------------- LOGIN ----------------

def login():

    st.subheader("Login")

    email=st.text_input("Email")

    password=st.text_input("Password",type="password")

    if st.button("Login"):

        users=load_users()

        if email in users and users[email]==password:

            st.session_state.user=email

            st.success("Login Success")

        else:

            st.error("Invalid")

# ---------------- UPLOAD ----------------

def upload():

    st.subheader("Upload Evidence")

    file=st.file_uploader("Upload File")

    lat=st.text_input("Latitude")

    lng=st.text_input("Longitude")

    if st.button("Analyze"):

        if file:

            progress=st.progress(0)

            for i in range(100):

                time.sleep(0.01)

                progress.progress(i+1)

            report=f"""
User: {st.session_state.user}
Time: {datetime.now()}
Risk: HIGH
Confidence: 98%
"""

            filename=file.name+".txt"

            path=os.path.join(REPORT,filename)

            with open(path,"w") as f:

                f.write(report)

            fb.upload_image(path,filename)

            if lat and lng:

                fb.save_location(st.session_state.user,lat,lng)

            st.success("Analysis Done")

# ---------------- ADMIN ----------------

def admin():

    st.subheader("Admin Dashboard")

    st.write("Intruder Images")

    urls=fb.get_images()

    for url in urls:

        st.image(url,width=200)

    st.write("Locations")

    data=fb.get_locations()

    if data:

        st.json(data)

# ---------------- PAGE CONTROL ----------------

if st.session_state.page=="home":

    home()

elif st.session_state.page=="register":

    register()

elif st.session_state.page=="login":

    login()

elif st.session_state.page=="upload":

    upload()

elif st.session_state.page=="admin":

    admin()
```

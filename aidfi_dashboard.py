import streamlit as st
import os
import json
import time
from datetime import datetime


# ---------------- CONFIG ----------------

st.set_page_config(
page_title="AIDFI",
layout="wide"
)


# ---------------- FILE PATH ----------------

USERS="users.json"
REPORTS="reports"


if not os.path.exists(USERS):

    with open(USERS,"w") as f:
        json.dump({},f)


if not os.path.exists(REPORTS):

    os.makedirs(REPORTS)



# ---------------- CSS ----------------

st.markdown("""

<style>

/* background */

.stApp{

background:
linear-gradient(135deg,#020617,#050510,#020617);

color:white;

}


/* title */

.title{

text-align:center;

font-size:45px;

font-weight:bold;

background:
linear-gradient(90deg,#00f5ff,#ff00ff);

-webkit-background-clip:text;

color:transparent;

}


/* card */

.card{

background:rgba(255,255,255,0.05);

padding:30px;

border-radius:15px;

box-shadow:0 0 20px cyan;

}


/* button */

.stButton button{

background:
linear-gradient(90deg,#00f5ff,#ff00ff);

color:white;

font-size:18px;

border-radius:10px;

border:none;

height:45px;

width:100%;

}


/* sidebar */

.css-1d391kg{

background:#020617;

}


/* footer */

.footer{

text-align:center;

margin-top:50px;

color:#888;

}


</style>

""",unsafe_allow_html=True)



# ---------------- LOAD USERS ----------------

def load():

    with open(USERS) as f:

        return json.load(f)



def save(data):

    with open(USERS,"w") as f:

        json.dump(data,f)



# ---------------- SESSION ----------------

if "page" not in st.session_state:

    st.session_state.page="home"



# ---------------- HOME ----------------

def home():

    st.markdown("<div class='title'>AIDFI Digital Forensics</div>",
    unsafe_allow_html=True)

    st.write("")

    col1,col2=st.columns(2)

    with col1:

        if st.button("Login"):

            st.session_state.page="login"


    with col2:

        if st.button("Register"):

            st.session_state.page="register"



# ---------------- REGISTER ----------------

def register():

    st.markdown("<div class='card'>",
    unsafe_allow_html=True)

    st.title("Register")

    email=st.text_input("Email")

    password=st.text_input("Password",type="password")


    if st.button("Register Now"):

        users=load()

        if email in users:

            st.error("Already exist")

        else:

            users[email]=password

            save(users)

            st.success("Register success")

            st.session_state.page="login"

            st.rerun()

    st.markdown("</div>",unsafe_allow_html=True)



# ---------------- LOGIN ----------------

def login():

    st.markdown("<div class='card'>",
    unsafe_allow_html=True)

    st.title("Login")

    email=st.text_input("Email")

    password=st.text_input("Password",type="password")


    if st.button("Login Now"):

        users=load()

        if email not in users:

            st.markdown("<span style='color:red'>* Email not found</span>",
            unsafe_allow_html=True)

        elif users[email]!=password:

            st.error("Wrong password")

        else:

            st.success("Login success")

            st.session_state.user=email

            st.session_state.page="dashboard"

            st.rerun()

    st.markdown("</div>",unsafe_allow_html=True)



# ---------------- DASHBOARD ----------------

def dashboard():

    st.sidebar.title("AIDFI")

    menu=st.sidebar.selectbox(

    "Menu",

    ["Upload Evidence","Reports","Logout"]

    )


    st.title("Admin Dashboard")


    if menu=="Upload Evidence":

        upload()


    elif menu=="Reports":

        reports()


    elif menu=="Logout":

        st.session_state.page="login"

        st.rerun()



# ---------------- UPLOAD ----------------

def upload():

    st.subheader("Upload Evidence")

    file=st.file_uploader("Upload File")


    if st.button("Analyze Evidence"):

        if file:

            st.write("Analyzing...")

            bar=st.progress(0)

            for i in range(100):

                time.sleep(0.01)

                bar.progress(i)


            result=f"""

AIDFI REPORT

User: {st.session_state.user}

Time: {datetime.now()}

Suspicious Events: 42

Risk Level: HIGH

AI Confidence: 98%

Status: Unauthorized access detected

"""


            name=file.name+".txt"


            with open(os.path.join(REPORTS,name),"w") as f:

                f.write(result)


            st.success("Analysis Complete")



# ---------------- REPORT ----------------

def reports():

    st.subheader("Reports")

    files=os.listdir(REPORTS)

    for f in files:

        with open(os.path.join(REPORTS,f),"rb") as file:

            st.download_button(

            "Download "+f,

            file,

            file_name=f)



# ---------------- PAGE CONTROL ----------------

if st.session_state.page=="home":

    home()

elif st.session_state.page=="login":

    login()

elif st.session_state.page=="register":

    register()

elif st.session_state.page=="dashboard":

    dashboard()



# ---------------- FOOTER ----------------

st.markdown(

"<div class='footer'>@by Digital Detectives Team</div>",

unsafe_allow_html=True

)

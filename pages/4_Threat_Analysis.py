import streamlit as st
import firebase_config as fb

st.title("Threat Analysis")

file=st.file_uploader("Upload File")

if st.button("Scan"):

    if file:

        st.error("Threat Detected")

        fb.upload_file(file.name,file.name)

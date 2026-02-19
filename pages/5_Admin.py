import streamlit as st
import firebase_config as fb

st.title("Admin Panel")

st.write(fb.get_files())

st.json(fb.get_locations())

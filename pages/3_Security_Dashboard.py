import streamlit as st
import firebase_config as fb

st.title("Security Dashboard")

st.metric("Threat Files",len(fb.get_files()))

st.metric("Tracked Devices",len(fb.get_locations()))

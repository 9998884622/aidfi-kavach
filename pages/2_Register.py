import streamlit as st
import json

st.title("Register")

email=st.text_input("Email")

password=st.text_input("Password",type="password")

if st.button("Register"):

    with open("users.json") as f:

        users=json.load(f)

    users[email]=password

    with open("users.json","w") as f:

        json.dump(users,f)

    st.success("Registered")

import streamlit as st

st.title("🛡 AIDFI – AI Digital Forensics Investigator")

file = st.file_uploader("Upload Log File")

if file:
    data = file.read().decode()

    if "failed" in data.lower():
        st.error("⚠ Failed Login Attempts Detected")
        st.write("AI Conclusion: Possible Brute Force Attack")

    elif "unauthorized" in data.lower():
        st.error("⚠ Unauthorized Access Detected")

    else:
        st.success("✅ No Threat Found")

    st.download_button("Download Report", "AIDFI Report Generated")

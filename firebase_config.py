import streamlit as st
import firebase_admin
from firebase_admin import credentials, storage, db

cred_dict = {
    "type": st.secrets["FIREBASE_TYPE"],
    "project_id": st.secrets["FIREBASE_PROJECT_ID"],
    "private_key_id": st.secrets["FIREBASE_PRIVATE_KEY_ID"],
    "private_key": st.secrets["FIREBASE_PRIVATE_KEY"].replace("\\n", "\n"),
    "client_email": st.secrets["FIREBASE_CLIENT_EMAIL"],
    "client_id": st.secrets["FIREBASE_CLIENT_ID"],
    "auth_uri": st.secrets["FIREBASE_AUTH_URI"],
    "token_uri": st.secrets["FIREBASE_TOKEN_URI"],
    "auth_provider_x509_cert_url": st.secrets["FIREBASE_AUTH_PROVIDER_X509_CERT_URL"],
    "client_x509_cert_url": st.secrets["FIREBASE_CLIENT_X509_CERT_URL"]
}

cred = credentials.Certificate(cred_dict)

firebase_admin.initialize_app(cred, {
    'storageBucket': f'{st.secrets["FIREBASE_PROJECT_ID"]}.appspot.com',
    'databaseURL': f'https://{st.secrets["FIREBASE_PROJECT_ID"]}.firebaseio.com/'
})

bucket = storage.bucket()
ref = db.reference('intruder_data')

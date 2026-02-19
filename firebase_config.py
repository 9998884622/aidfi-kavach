import firebase_admin
from firebase_admin import credentials, storage, db
from datetime import datetime

cred = credentials.Certificate("firebase_service_account.json")  # Replace with your service account
firebase_admin.initialize_app(cred, {
    'storageBucket': 'your-project-id.appspot.com',   # Replace
    'databaseURL': 'https://your-project-id.firebaseio.com/'  # Replace
})

bucket = storage.bucket()
ref = db.reference('intruder_data')

def upload_intruder_image(file_path, filename):
    blob = bucket.blob(f"intruder/{filename}")
    blob.upload_from_filename(file_path)
    return blob.public_url

def save_location(user_id, lat, lng):
    ref.child(user_id).set({'lat': lat, 'lng': lng})

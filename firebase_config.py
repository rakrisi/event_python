import firebase_admin
from firebase_admin import credentials, firestore
import os
from datetime import datetime

class FirebaseDB:
    def __init__(self):
        # Initialize Firebase Admin SDK
        # You'll need to download your service account key JSON file from Firebase Console
        # and set the path in the environment variable or place it in the project directory
        
        service_account_path = os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY', 'firebase-service-account-key.json')
        
        if not firebase_admin._apps:
            try:
                cred = credentials.Certificate(service_account_path)
                firebase_admin.initialize_app(cred)
            except Exception as e:
                print(f"Error initializing Firebase: {e}")
                print("Please ensure you have downloaded the service account key file from Firebase Console")
                print("and either set FIREBASE_SERVICE_ACCOUNT_KEY environment variable or place it as 'firebase-service-account-key.json'")
                raise
        
        self.db = firestore.client()
    
    def get_db(self):
        return self.db

# Global Firebase instance
firebase_db = FirebaseDB()

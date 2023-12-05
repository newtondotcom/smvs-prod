import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

default_app = firebase_admin.initialize_app()
db = firestore.client()

doc_ref = db.collection("users").document("abc")


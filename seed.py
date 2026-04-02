import json
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

with open("seed_data/doctors.json") as f:
    doctors = json.load(f)

for doc in doctors:
    db.collection("doctors").document(doc["id"]).set(doc)
    print(f"Seeded: {doc['name']}")

print("Done! Firestore seeded.")

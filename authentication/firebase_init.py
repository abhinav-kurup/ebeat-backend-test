import firebase_admin
from firebase_admin import credentials
from django.conf import settings

firebase_path = f"{settings.BASE_DIR}firebase.json"
firebase_cred = credentials.Certificate(firebase_path)
firebase_admin.initialize_app(firebase_cred)


# print(firebase_path)

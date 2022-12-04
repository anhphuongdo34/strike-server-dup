import firebase_admin
from firebase_admin import credentials, firestore


def getDb() :
    databaseURL = "https://strike-depauw-default-rtdb.firebaseio.com/"
    cred_obj = credentials.Certificate('./data/firebaseServiceKey.json')
    default_app = firebase_admin.initialize_app(cred_obj)
    db = firestore.client(default_app)
    return db
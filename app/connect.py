import firebase_admin
from firebase_admin import credentials, db
import socket

class Communicate:
    def __init__(self, private_key="./certs/admin-key.json", firebase_url="https://spirobot-d9387.firebaseio.com/"):
        firebase_admin.initialize_app(credentials.Certificate(private_key), {
            "databaseURL": firebase_url
        })
        self.ref = db.reference("/")
        self.ping = db.reference("ping")


    def ping(self):
        self.ping.set(True)

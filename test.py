import pyrebase
config = {
    "apiKey": "AIzaSyCNqP7QA-spg2B-WblSnbJ9kcVLntvSq_Q",
    "authDomain": "nisb-ieee.firebaseapp.com",
    "databaseURL": "https://nisb-ieee.firebaseio.com",
    "projectId": "nisb-ieee",
    "storageBucket": "",
    "messagingSenderId": "496074877089"
}
firebase  = pyrebase.initialize_app(config)
db = firebase.database()
db.child("Name").push("OKay")
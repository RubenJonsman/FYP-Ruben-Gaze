import firebase_admin
from firebase_admin import credentials
from firebase_admin import db



class DB_Helper():
    # Definere nøglen til databasen
    cred = credentials.Certificate('eyetracking-1e270-firebase-adminsdk-zfrrm-f5700d4099.json')

    # Initialisere databasen
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://eyetracking-1e270.firebaseio.com/'
    })

    # Funktion til at uploade de ord som brugeren har skrevet til databasen
    def INSERTDATA(self, data):
        # Definere tom string
        insert = ""

        # Hvis længden på dataen er 1, sættes insert = dataen
        if len(data) == 1:
            insert = data[0]

        # Ellers konveteres hvert bogstav i data til en samlet string
        else:
            for char in str(data):
                insert += char + " "
            
        # Definere, databasens reference
        ref = db.reference('')
        users_ref = ref
        # Indsætter stringen insert i databasen under kolonnen ved navn MessageData
        users_ref.set({
            "MessageData": insert
        })



    # Funktion til at uploade ordlisten til databasen
    def INSERTWL(self, word_list):
        # Definere en tom string
        insert = ""

        # Konvetere word_list til en samlet string
        for char in word_list:
            insert += char + " "

        # Stringen uploades til databasen under kolonnen ved navn WordListData
        ref = db.reference('')
        users_ref = ref
        users_ref.set({
            "WordListData": insert
        })

        



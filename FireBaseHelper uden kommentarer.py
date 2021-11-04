import firebase_admin
from firebase_admin import credentials
from firebase_admin import db



class DB_Helper():

    cred = credentials.Certificate('eyetracking-1e270-firebase-adminsdk-zfrrm-f5700d4099.json')


    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://eyetracking-1e270.firebaseio.com/'
    })


    def INSERTDATA(self, data):

        insert = ""


        if len(data) == 1:
            insert = data[0]


        else:
            for char in str(data):
                insert += char + " "
            

        ref = db.reference('')
        users_ref = ref

        users_ref.set({
            "MessageData": insert
        })




    def INSERTWL(self, word_list):

        insert = ""


        for char in word_list:
            insert += char + " "


        ref = db.reference('')
        users_ref = ref
        users_ref.set({
            "WordListData": insert
        })

        



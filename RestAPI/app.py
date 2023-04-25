from flask import Flask, request
from flask_cors import CORS
from config import db_config, firebase_config
from psycopg2 import connect
import pyrebase 

app = Flask(__name__)
app.secret_key = "secret key"
CORS(app)

conn = connect(**db_config)
cur = conn.cursor()

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

                
@app.route('/login', methods=['POST'])
def login(): 
    email = request.json['email']
    password = request.json['password']
    try:
        auth.sign_in_with_email_and_password(email, password)
        return 'Logged in successfully'
    except Exception as e:
        return 'Error in logging in: ' + str(e)
    
if __name__ == '__main__':
    app.run(port=5000,debug=True)
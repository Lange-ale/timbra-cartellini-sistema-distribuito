from flask import Flask, request
from flask_cors import CORS
from config import db_config, firebase_config
from repository.worker import WorkerRepository
from psycopg2 import connect
import pyrebase 
from functools import wraps
    
app = Flask(__name__)
app.secret_key = "secret key"
CORS(app)

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

conn = connect(**db_config)
worker_repository = WorkerRepository(conn)


def token_required(f):
    @wraps(f)
    def check_token(*args, **kwargs):
        if 'token' not in request.headers:
            return 'Token is missing', 401
        token = request.headers['token']       
        try:
            request.user = auth.get_account_info(token) ['users'][0]
        except:
            return 'Token is invalid', 401
        return f(*args, **kwargs)
    return check_token

                
@app.route('/token', methods=['POST'])
def get_token(): 
    email = request.json['email']
    password = request.json['password']
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        token = user['idToken']
        return {'token': token}, 200
    except Exception as e:
        return {'error': str(e)}, 400
    
    
@app.route('/worker', methods=['GET'])
@token_required 
def get_worker():
    email = request.user['email']
    worker = worker_repository.get_by_email(email)
    if worker is None:
        return 'Worker not found', 404
    return worker



if __name__ == '__main__':
    app.run(port=5000,debug=True)
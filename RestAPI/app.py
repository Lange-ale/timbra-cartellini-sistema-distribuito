from flask import Flask, request
from flask_cors import CORS
from config import db_config, firebase_config
from repository.worker import WorkerRepository
from repository.log import LogRepository
from psycopg2 import connect
import pyrebase 
from functools import wraps
from time import sleep
    
app = Flask(__name__)
app.secret_key = "secret key"
CORS(app)

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

err = 1
while err is not None:
    try:
        conn = connect(**db_config)
        err = None
    except Exception as e:
        print(e)
        err = e
        sleep(1)


worker_repository = WorkerRepository(conn)
log_repository = LogRepository(conn)


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
        return {'error': 'Worker not found'}, 404
    return worker.__dict__, 200


@app.route('/timbra', methods=['POST'])
@token_required
def timbra(): # return the log registered
    email = request.user['email']
    worker = worker_repository.get_by_email(email)
    if worker is None:
        return {'error': 'Worker not found'}, 404
    last = log_repository.last_is_an_entry(worker.uuid)
    if last is None:
        last = False
    new_log = log_repository.insert(worker.uuid, not last)
    return new_log.__dict__, 200    


@app.route('/logs/last_is_an_entry', methods=['GET'])
@token_required
def last_is_an_entry():
    email = request.user['email']
    worker = worker_repository.get_by_email(email)
    if worker is None:
        return {'error': 'Worker not found'}, 404
    last = log_repository.last_is_an_entry(worker.uuid)
    if last is None:
        return {'error': 'Log not found'}, 404
    return {'last_is_an_entry': last}, 200


@app.route('/logs', methods=['GET'])
@token_required
def get_logs():
    email = request.user['email']
    worker = worker_repository.get_by_email(email)
    if worker is None:
        return {'error': 'Worker not found'}, 404
    logs = log_repository.get_by_worker(worker.uuid)
    return {'logs': [log.__dict__ for log in logs]}, 200
    

@app.route('/', methods=['GET'])
def hello():
    return 'Hello'

if __name__ == '__main__':
    app.run(port=5000,debug=True)
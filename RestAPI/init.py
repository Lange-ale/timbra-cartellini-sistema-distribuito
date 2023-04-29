from config import firebase_config, db_config
from fake_data import accounts, logs

# before running this script run "docker-compose up --build" to start the database
# and run "pip install -r requirements.txt" to install the required packages

print("Do you want to create the accounts on firebase? (y/n)")
answer = input()
if answer.lower() != "y":
    print("The accounts will not be created on firebase")
else:
    import pyrebase
    
    firebase = pyrebase.initialize_app(firebase_config)
    auth = firebase.auth()    

    for email, account in accounts.items():
        try:
            auth.create_user_with_email_and_password(email, account["password"])
            print("Account created for " + email)
        except Exception as e:
            print("Error: " + str(e))
    
    print("Done")
    
    
print("Do you want to create the accounts on the database? (y/n)")
answer = input()
if answer.lower() != "y":
    print("The accounts will not be created on the database")
else:
    from psycopg2 import connect

    conn = connect(**db_config)
    cur = conn.cursor()

    cur.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    cur.execute('DROP TABLE IF EXISTS workers')
    cur.execute(
        """ CREATE TABLE workers (
            uuid VARCHAR(255) PRIMARY KEY DEFAULT uuid_generate_v4(),
            email VARCHAR(255) NOT NULL UNIQUE,
            name VARCHAR(255) NOT NULL,
            surname VARCHAR(255) NOT NULL,
            entrance_time TIME NOT NULL,
            exit_time TIME NOT NULL
        )""" 
    )
    
    for email, account in accounts.items():
        cur.execute(f"""INSERT INTO workers (uuid, email, name, surname, entrance_time, exit_time) 
                        VALUES ('{account['uuid']}', '{email}', '{account['name']}', '{account['surname']}', 
                        '{account['entrance_time']}', '{account['exit_time']}')""")
                    
    cur.execute('DROP TABLE IF EXISTS logs')
    cur.execute(
        """ CREATE TABLE logs (
            uuid VARCHAR(255) PRIMARY KEY DEFAULT uuid_generate_v4(),
            date DATE NOT NULL,
            clock_in TIME NOT NULL,
            clock_out TIME NOT NULL,
            uuid_worker VARCHAR(255) NOT NULL,
            
            CONSTRAINT fk_worker
                FOREIGN KEY(uuid_worker)
                REFERENCES workers(uuid)
                ON DELETE CASCADE
        )""" 
    )
    
    for uuid, log in logs.items():
        cur.execute(f"""INSERT INTO logs (uuid, date, clock_in, clock_out, uuid_worker) 
                        VALUES ('{uuid}', '{log['date']}', '{log['clock_in']}', '{log['clock_out']}', 
                        '{log['uuid_worker']}')""")
    
    conn.commit()

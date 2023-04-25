from config import firebase_config, db_config, accounts

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
            surname VARCHAR(255) NOT NULL
        )""" 
    )
    
    for email, account in accounts.items():
        cur.execute("INSERT INTO workers (email, name, surname) VALUES (%s, %s, %s)", (email, account["name"], account["surname"]))
    
    conn.commit()

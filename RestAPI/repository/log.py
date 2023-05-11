from datetime import datetime
from os import environ
environ['TZ'] = 'Europe/Rome'

class Log:
    def __init__(self, uuid, date, time, is_entry, uuid_worker):
        self.uuid = uuid
        self.date = date.strftime("%Y-%m-%d")
        self.time = time.strftime("%H:%M:%S")
        self.is_entry = is_entry
        self.uuid_worker = uuid_worker
    
class LogDTO:
    def __init__(self, date, time, is_entry, uuid_worker):
        self.date = date.strftime("%Y-%m-%d")
        self.time = time.strftime("%H:%M:%S")
        self.is_entry = is_entry
        self.uuid_worker = uuid_worker
        
class LogRepository:
    def __init__(self, conn):
        self.conn = conn
        self.cur = conn.cursor()
        
    def get_by_worker(self, uuid_worker):
        self.cur.execute("SELECT * FROM logs WHERE uuid_worker = %s ORDER BY date DESC, time DESC", (uuid_worker,))
        logs = self.cur.fetchall()
        if logs is None:
            return None
        return [Log(*log) for log in logs]
        
    def last_is_an_entry(self, uuid_worker):
        self.cur.execute("SELECT is_entry FROM logs WHERE uuid_worker = %s ORDER BY date DESC, time DESC LIMIT 1", (uuid_worker,))
        log = self.cur.fetchone()
        if log is None:
            return None
        return log[0]
        
    def insert(self, uuid_worker, is_entry):
        #set the it to the current date and time
        date = datetime.today().strftime('%Y-%m-%d')
        time = datetime.today().strftime('%H:%M:%S.%f')[:-3]
        self.cur.execute("INSERT INTO logs (date, time, is_entry, uuid_worker) VALUES (%s, %s, %s, %s) RETURNING *", (date, time, is_entry, uuid_worker))
        log = self.cur.fetchone()
        self.conn.commit()
        return Log(*log)


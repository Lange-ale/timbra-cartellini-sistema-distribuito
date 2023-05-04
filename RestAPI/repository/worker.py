class Worker:
    def __init__(self, uuid, email, name, surname, entrance_time, exit_time):
        self.uuid = uuid
        self.email = email
        self.name = name
        self.surname = surname
        self.entrance_time = entrance_time.strftime("%H:%M:%S")
        self.exit_time = exit_time.strftime("%H:%M:%S")

class WorkerDTO:
    def __init__(self, email, name, surname, entrance_time, exit_time):
        self.email = email
        self.name = name
        self.surname = surname
        self.entrance_time = entrance_time.strftime("%H:%M:%S")
        self.exit_time = exit_time.strftime("%H:%M:%S")
        
   
class WorkerRepository:
    def __init__(self, conn):
        self.conn = conn
        self.cur = conn.cursor()

        
        
    def get_by_email(self, email):
        self.cur.execute("SELECT * FROM workers WHERE email = %s", (email,))
        worker = self.cur.fetchone()
        if worker is None:
            return None
        return Worker(*worker)
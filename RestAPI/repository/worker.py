class Worker:
    def __init__(self, uuid, email, name, surname):
        self.uuid = uuid
        self.email = email
        self.name = name
        self.surname = surname

class WorkerDTO:
    def __init__(self, email, name, surname):
        self.email = email
        self.name = name
        self.surname = surname
        
   
class WorkerRepository:
    def __init__(self, conn):
        self.conn = conn
        self.cur = conn.cursor()
        
    def get_by_email(self, email):
        self.cur.execute("SELECT * FROM workers WHERE email = %s", (email,))
        worker = self.cur.fetchone()
        if worker is None:
            return None
        return Worker(*worker).__dict__
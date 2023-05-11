class Worker:
    def __init__(self, uuid, email, name, surname, entrance_time, exit_time, is_admin):
        self.uuid = uuid
        self.email = email
        self.name = name
        self.surname = surname
        self.entrance_time = entrance_time.strftime("%H:%M:%S")
        self.exit_time = exit_time.strftime("%H:%M:%S")
        self.is_admin = is_admin

class WorkerDTO:
    def __init__(self, email, name, surname, entrance_time, exit_time, is_admin):
        self.email = email
        self.name = name
        self.surname = surname
        self.entrance_time = entrance_time.strftime("%H:%M:%S")
        self.exit_time = exit_time.strftime("%H:%M:%S")
        self.is_admin = is_admin
   
class WorkerRepository:
    def __init__(self, conn):
        self.conn = conn
        self.cur = conn.cursor()

        
        
    def get_by_email(self, email):
        self.cur.execute(f''' SELECT uuid,
                                     email,
                                     name,
                                     surname,
                                     entrance_time,
                                     exit_time,
                                     is_admin
                                FROM workers WHERE email = '{email}' ''')
        worker = self.cur.fetchone()
        if worker is None:
            return None
        return Worker(*worker)
    
    
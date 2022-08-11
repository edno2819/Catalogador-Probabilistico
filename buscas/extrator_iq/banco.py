import psycopg2

class DataBaseClass:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conect()
        self.limite = 15000
    
    def conect(self):
        self.mydb  =  psycopg2.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database
            )

        self.cur = self.mydb.cursor()

    def create_database(self, name):
      self.cur.execute(f"CREATE DATABASE IF NOT EXISTS{name}")
        

    def create_table(self, table):
        self.cur.execute(f'''CREATE TABLE IF NOT EXISTS {table} (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                                                nome text (32),
                                                                data TEXT
                                                                )''')


    def show_tables(self):
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        try:
            self.cur.execute(query)
        except:
            self.conect()
            self.cur.execute(query)


    def insert_data(self, tabela:str,  new_data:str, columns:str=''):
        query = f'''INSERT INTO {tabela} {columns} VALUES {new_data}'''
        try:
            self.cur.execute(query)
        except:
            self.conect()
            self.cur.execute(query)

    def get_data(self, codigo:str):
        self.cur.execute(codigo)
        return self.cur.fetchall()
    
    def trys(self, func):
        try:
            func()
        except:
            self.reconnect()
    
    def reverErro(self):
        self.cur.execute("ROLLBACK")


    def close(self):
      self.mydb.close()

    def check_connected(self):
      self.mydb.is_connected()
    
    def reconnect(self):
        if not self.check_connected:
            self.conect()

    def commit(self):
      self.mydb.commit()


                        
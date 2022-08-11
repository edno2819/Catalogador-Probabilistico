import mysql.connector
from datetime import date

class MysqlClass:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conect()
        self.limite = 150000
    
    def conect(self):
        self.mydb  =  mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database
            )

        self.cur = self.mydb.cursor(buffered=True)

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
        

    def show_table(self, table):
        query = f'select * from {table}'
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


    def get_data_by_colum_filter(self, tabela:str, colum:str, search:str, itens:str='*', date_range=(date(2021, 1, 5), date.today())):
        query = f'''
                    select {itens} from {tabela} where 
                    ({colum} like "%{search}%") AND (OrderDate >= "{date_range[0]}") AND 
                    (OrderDate <= "{date_range[1]}") ORDER BY ID DESC limit {self.limite}
                '''
        try:
            self.cur.execute(query)
        except:
            self.conect()
            self.cur.execute(query)

        return self.cur.fetchall()


    def get_all_data_from_table(self, tabela:str, coluns:str='*'):
        query = f'''select {coluns} from {tabela}'''
        try:
            self.cur.execute(query)
        except:
            self.conect()
            self.cur.execute(query)

        return self.cur.fetchall()


    def get_data(self, codigo:str):
        self.cur.execute(codigo)
        return self.cur.fetchall()


    def close(self):
        self.mydb.close()

    def check_connected(self):
      return self.mydb.is_connected()
    
    def execTry(self, query, n=5):
        for c in range(n):
            try:
                try:
                    self.cur.execute(query)
                except:
                    self.reconnect()
                    self.cur.execute(query)
                self.commit()
                return True
            except:
                return False

    def reconnect(self):
        if not self.check_connected:
            self.conect()

    def commit(self):
        self.mydb.commit()


                        
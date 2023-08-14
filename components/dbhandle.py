import os
import sys
path = os.path.abspath('./')
sys.path.append(path)
from mysql.connector import  connect, Error
from components.filehandle import File

class Database():
    def __init__(self):
        self.connection_error = False
        self.file = File()
        self.first_connection = True
        self.connected =False
        self.message_connection_error = None
        self.get_file_config()
        
    def start_connection(self):
        self.connection_error = False
        self.get_file_config()
        print(self.config)
        try:
            self.conexao = connect(**self.config)
            print(self.conexao)
            self.connected = True
            self.cursor = self.conexao.cursor()
            return True            
        except Error as er:
            self.connection_error = True
            self.connected = False
            self.message_connection_error = er
            print(er)
            return False
  
    def db_default_config(self):
        if self.verify_connection():
            if not self.connection_error:
                query = """
                    UPDATE clientes
                    SET email = '2teste.mais@gmail.com',
                        emailfinanceiro = '2teste.mais@gmail.com',
                        emailcte = '2teste.mais@gmail.com',
                        emailnfe = '2teste.mais@gmail.com';

                    UPDATE empresas
                    SET email = '2teste.mais@gmail.com';

                    UPDATE contabilista
                    SET Email = '2teste.mais@gmail.com',
                        EmailXmlEnvio = '2teste.mais@gmail.com';

                    UPDATE USUARIOS set Password = 'W'

                """
                query_return = self.execute_query(query)
                if query_return == 'sucess':
                    return 'sucess'
                else:
                    return query_return
                
            else:
                self.connected = False
                return self.message_connection_error
        else:
            return 'banco de dados desconectado'
    
    def reset_users_password(self):
        if self.verify_connection():
            if not self.connection_error:
                query = """
                    UPDATE USUARIOS set Password = 'W'
                """
                query_return = self.execute_query(query)
                if query_return == 'sucess':
                    return 'sucess'
                else:
                    return query_return
            else:
                return self.message_connection_error
        else:
            self.connected = False
            return 'banco de dados desconectado'
        
    def execute_query(self, query):
        has_connection = self.verify_connection()
        if has_connection:
            try:
                self.cursor.execute(query)
                self.cursor.close()
                self.conexao.close()
                self.connected = False
                return 'sucess'
            except Error as er:
                return er
        else:
            self.connected = False
            Exception ("banco de dados desconectado")
            return self.message_connection_error

    def execute_query_return(self, query):
        has_connection = self.verify_connection()
        if has_connection:
            try:
                self.cursor.execute(query)
                self.connected = False
                return 'sucess',self.cursor.fetchall()
            except Error as er:
                return 'error', er
        else:
            self.connected = False
            Exception ("banco de dados desconectado")
            return self.message_connection_error
            
    def verify_connection(self):
        if self.first_connection:
            connection = self.start_connection()
            if connection:
                self.first_connection = False
                return True
            else: 
                return False
        else: 
            if self.connected:
                return True
            else:
                connection = self.start_connection()
                if connection:
                    return True
                else:
                    return False
            
    def get_file_config(self):
        self.config = self.file.read_json()

if __name__ == "__main__":
    import re
    db = Database()
    # print(db.db_default_config())
    
    query = 'SELECT * FROM USUARIOS'
    pattern = re.compile(r'select', re.IGNORECASE)
    match = pattern.search(query)
    if match:
        print(db.execute_query_return(query))
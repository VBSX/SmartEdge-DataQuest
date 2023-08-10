from mysql.connector import  connect, Error
from filehandle import File

class Database():
    def __init__(self):
        self.connection_error = False
        self.config = File()
        self.first_connection = True
        self.config = self.config.json_file
        # config = {
        #     'user': 'root',
        #     'password': 'vssql',
        #     'host': '10.1.1.220',  
        #     'port': 3307,
        #     'database': '10861-1'
        # }
        

            
    def start_connection(self):
        try:
            self.conexao = connect(**self.config)
            
            self.cursor = self.conexao.cursor()
            
        except Error as er:
            self.connection_error = True
            self.message_connection_error = er
            print(er)
  
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
            return 'banco de dados desconectado'
    def execute_query(self, query):
        if self.verify_connection():
            self.cursor.execute(query)
            self.cursor.close()
            self.conexao.close()
            return 'sucess'
        else:
            Exception ("banco de dados desconectado")
    
    def verify_connection(self):
        if self.first_connection:
            self.start_connection()
            return True
        else:
            if self.conexao.connected():
                return True
            else:
                return False
        
if __name__ == "__main__":
    db = Database()
    print(db.db_default_config())
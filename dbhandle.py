import mysql.connector
class Database():
    def __init__(self) -> None:
        config = {
            'user': 'root',
            'password': 'vssql',
            'host': '10.1.1.220',  
            'port': 3307,
            'database': '10861-1'
        }
        self.conexao = mysql.connector.connect(**config)
        self.cursor = self.conexao.cursor()
  
    def db_default_config(self):
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
        self.execute_query(query)
        
    def execute_query(self, query):
        self.cursor.execute(query)
        self.cursor.close()
        self.conexao.close()
if __name__ == "__main__":
    db = Database()
    print(db.db_default_config())
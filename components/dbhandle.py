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
        try:
            self.conexao = connect(**self.config)
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
                    update
                        clientes
                    set
                        TELEFONE1 = '999999999',
                        TELEFONE2 = '999999999',
                        FAX = '999999999',
                        ENT_FAX = '999999999';
                        email = '2teste.mais@gmail.com',
                        EMAILCONTATO,
                        EMAILCOMPRADOR,
                        emailfinanceiro = '2teste.mais@gmail.com',
                        emailcte = '2teste.mais@gmail.com',
                        emailnfe = '2teste.mais@gmail.com',
                        EMAILSOCIO1,
                        EMAILSOCIO2,
                        EMAILSOCIO3,
                        EMAILSOCIO4,
                        ENT_EMAIL 
                    UPDATE empresas
                    SET email = '2teste.mais@gmail.com';

                    UPDATE contabilista
                    SET Email = '2teste.mais@gmail.com',
                        EmailXmlEnvio = '2teste.mais@gmail.com';

                    UPDATE USUARIOS set Password = 'W';
                    
                """
                query_return2 = self.update_password_supervisor()
                query_return = self.execute_query(query)
                
                if query_return and query_return2 == 'sucess':
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
                    UPDATE USUARIOS set Password = 'W';
                """
                query_return = self.execute_query(query)
                query_return_supervisor = self.update_password_supervisor() 
                query2 = """
                    UPDATE USUARIOS_SUPERVISORES 
                    SET 
                    Lib_Desconto = '1',
                    Lib_Credito = '1';
                """
                query_return2 = self.execute_query(query2)
                if query_return and query_return_supervisor and query_return2 == 'sucess':
                    return 'sucess'
                else:
                    return query_return +f'\n{query_return_supervisor}'
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
                try:
                    self.conexao.commit()
                except:
                    pass
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
    
    def execute_query_for_multiple_querys(self,query_list):
        
        has_connection = self.verify_connection()
        if has_connection:
            try:
                for query in query_list:
                    self.cursor.execute(query)
                    self.conexao.commit()
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
        
    def update_password_supervisor(self):
        query_sequence = "SELECT Sequencia FROM USUARIOS_SUPERVISORES;"
        sequence = self.execute_query_return(query_sequence)
        sequence_raw = sequence[1]
        sequence = []
        list_query = []
        
        for item in sequence_raw:
            item = str(item)
            item = item.replace(',', '').replace('(', '').replace(')', '')
            sequence.append(int(item))
           
        for index, row in enumerate(sequence_raw):
            row = row[0]
            password_value = row*4
            query = f"UPDATE USUARIOS_SUPERVISORES SET Password = '{password_value}' WHERE Sequencia = {row};"
            list_query.append(query)
        return self.execute_query_for_multiple_querys(list_query)
    
    def get_file_config(self):
        self.config = self.file.read_json(database=True)

    def import_sovis_order(self, idpedido):
        query = f"""
            UPDATE PEDIDOSOVIS SET STATUSPEDIDO = 0 WHERE IDPEDIDO = {idpedido}
        """
        return self.execute_query_return(query)
    
    def get_sovis_order(self, idpedido):
        query = f"""
            SELECT IDPEDIDO FROM PEDIDOSOVIS WHERE IDPEDIDO = {idpedido}
        """
        return self.execute_query_return(query)
    
    def get_type_id_order_sovis (self, order_number):
        query = f"""
            SELECT IDTIPOPEDIDO FROM PEDIDOSOVIS WHERE IDPEDIDO = {order_number}
        """
        return self.execute_query_return(query)
    
    def update_type_id_order_sovis (self, order_number, type_id):
        query = f"""
            UPDATE PEDIDOSOVIS SET IDTIPOPEDIDO = {type_id} WHERE IDPEDIDO = {order_number}
        """
        return self.execute_query_return(query)
    
    def get_type_id_itens_order_sovis (self, order_number):
        query = f"""
            SELECT TIPO FROM ITEMPEDIDOSOVIS WHERE IDPEDIDO = {order_number}
        """
        return self.execute_query_return(query)
    
    def update_type_id_itens_order_sovis (self, order_number, type_id):
        query = f"""
            UPDATE ITEMPEDIDOSOVIS SET TIPO = {type_id} WHERE IDPEDIDO = {order_number}
        """
        return self.execute_query_return(query)
    
if __name__ == "__main__":
    
    db = Database()
    # print(db.db_default_config())
    # query = """
    #     UPDATE USUARIOS_SUPERVISORES set Password = '12231132'
        
    # """
    # print(db.execute_query(query))
    print(db.update_password_supervisor())
    
    # import re
    # pattern = re.compile(r'select', re.IGNORECASE)
    # match = pattern.search(query)
    # if match:
    #     print(db.execute_query_return(query))
from os.path import abspath as path_os
from sys import path as syspath
path = path_os('./')
syspath.append(path)
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
        self.config['charset'] = 'utf8mb4'
        self.config['collation'] = 'utf8mb4_general_ci'
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
            query_return = self.update_users_password_to_default()
            if query_return != 'sucess':
                return query_return
            else:
                query_return2 = self.update_password_supervisor()
                query_return3 = self.update_nfce_config_env_to_hml()
                query_return4 = self.update_phone_customer()
                query_return5 = self.update_emails_accountant()
                query_return6 = self.update_emails_customer()
                query_return7 =self.update_email_org()
                query_return8 = self.update_nfe_config_env_to_hml()
                
                list_query = [query_return, query_return2, query_return3, query_return4, query_return5, query_return6, query_return7, query_return8]
                for query in list_query:
                    if query != 'sucess':
                        return query
                    
                return 'sucess'  
    
    def update_users_password_to_default(self):
        query = """
            UPDATE 
                USUARIOS
            set
                Password = 'W';
        """
        return self.execute_query(query)
    
    def update_phone_customer(self):
        query = """
            update
                clientes
            set
                TELEFONE1 = '999999999',
                TELEFONE2 = '999999999',
                FAX = '999999999',
                ENT_FAX = '999999999';
        """
        return self.execute_query(query)

    def update_emails_accountant(self):
        query = """
            update
                contabilista
            set
                Email = '2teste.mais@gmail.com',
                EmailXmlEnvio = '2teste.mais@gmail.com';
        """
        return self.execute_query(query)
    
    def update_emails_customer(self):
        query = """
            update
                clientes
            set
                email = '2teste.mais@gmail.com',
                EMAILCONTATO = '2teste.mais@gmail.com',
                EMAILCOMPRADOR = '2teste.mais@gmail.com',
                emailfinanceiro = '2teste.mais@gmail.com',
                emailcte = '2teste.mais@gmail.com',
                emailnfe = '2teste.mais@gmail.com',
                EMAILSOCIO1 = '2teste.mais@gmail.com',
                EMAILSOCIO2 = '2teste.mais@gmail.com',
                EMAILSOCIO3 = '2teste.mais@gmail.com',
                EMAILSOCIO4 = '2teste.mais@gmail.com',
                ENT_EMAIL = '2teste.mais@gmail.com';
        """
        return self.execute_query(query) 
    
    def update_email_org(self):
        query = """
            update
                empresas
            set
                email = '2teste.mais@gmail.com';
        """
        return self.execute_query(query)
    
    
    
    def reset_users_password(self):
            query_return = self.update_users_password_to_default()
            if query_return != 'sucess':
                return query_return
            else:
                query_return_supervisor = self.update_password_supervisor() 
                query_return2 = self.update_permission_supervisor()
                list_of_query = [query_return, query_return_supervisor, query_return2]
                for query in list_of_query:
                    if query != 'sucess':
                        return query
                return 'sucess'

    def update_permission_supervisor(self):
        query = """
            UPDATE USUARIOS_SUPERVISORES 
            SET 
                Lib_Desconto = '1',
                Lib_Credito = '1';
        """
        return self.execute_query(query)
        
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
        
        list_query = []
        if sequence[0] != 'error':
            sequence = []
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
        else: 
            return sequence[1]
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
        return self.execute_query(query)
    
    def get_nfce_config_env(self):
        query = """
        SELECT AMBIENTE FROM NFCE_CONFIG
        """
        return self.execute_query_return(query)
    
    def update_nfce_config_env_to_hml(self):
        query = """
        UPDATE 
            NFCE_CONFIG 
        SET 
            AMBIENTE = 2
        """
        return self.execute_query(query)
    
    def update_nfe_config_env_to_hml(self):
        query = """
            update
                NOTA_TAMANHO
            set
                NFE_AMBIENTE = 2
        """
        return self.execute_query(query)
        
if __name__ == "__main__":
    
    db = Database()
    print(db.db_default_config())

    # print(db.update_password_supervisor())
    # print(db.update_nfce_config_env_to_hml())


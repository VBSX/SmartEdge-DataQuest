import os
import sys
path = os.path.abspath('./')
sys.path.append(path)
import json
from components.ini_handle import IniConfig

class File():
    def __init__(self):
        self.ini_config = IniConfig()
        self.path_json = r'components/params.json'
        self.json_file = self.read_json()
        self.init_json_config_align_with_dotini()
        self.username = self.get_username()
        self.password = self.get_password()
        self.host = self.get_host()
        self.port = self.get_port()
        self.database = self.get_database()
    
    def create_json(self):
        if self.verify_if_json_exists():
            return False
        elif not self.verify_if_path_components_exist():
            self.create_components_path()
            self.create_defaut_json()
            return True
        else:
            self.create_defaut_json()
            return True
        
    def verify_if_json_exists(self):
        if os.path.exists(self.path_json):
            return True
        else:
            return False
    
    def read_json(self, database = False):
        if self.verify_if_json_exists():
                with open(self.path_json, 'r') as f:
                    content = json.load(f)
                if not database:
                    return content   
                else:
                    # retira os campos referente as credenciais do bitrix e forum
                    try:
                        content.pop('bitrix_user')
                        content.pop('bitrix_password')
                        content.pop('forum_user')
                        content.pop('forum_password')
                    except:
                        print('erro ao retirar os campos referente as credenciais do bitrix e forum')
                        
                    return content
                
        else:
            self.create_json()
            with open(self.path_json, 'r') as f:
                content = json.load(f)
                return content
    
    def init_json_config_align_with_dotini(self):
            host = self.ini_config.host_ini
            database = self.ini_config.database_ini
            port = self.ini_config.port_ini
            self.set_database(database)
            self.set_host(host)
            self.set_port(port)
            
            self.write_json()
               
    def get_username(self):
        if self.verify_if_json_exists():
            if self.json_file['user']:
                return self.json_file['user']
            else:
                return 'None'
        else:
            self.create_json()
    
    def get_password(self):
        if self.verify_if_json_exists():
            if self.json_file['password']:
                return self.json_file['password']
            else:
                return 'None'
        else:
            self.create_json()
            
    def get_host(self):
        if self.verify_if_json_exists():
            if self.json_file['host']:
                return self.json_file['host']
            else:
                return 'None'
        else:
            self.create_json()
            
    def get_port(self):
        if self.verify_if_json_exists():
            if self.json_file['port']:
                return self.json_file['port']
            else:
                return 'None'
        else:
            self.create_json()
            
    def get_port(self):
        if self.verify_if_json_exists():
            if self.json_file['port']:
                return self.json_file['port']
            else:
                return 'None'
        else:
            self.create_json()
            
    def get_database(self):
        if self.verify_if_json_exists():
            if self.json_file['database']:
                return self.json_file['database']
            else:
                return 'None'
        else:
            self.create_json()
    
    def get_bitrix_user(self):
        if self.verify_if_json_exists():
            if self.json_file['bitrix_user']:
                return self.json_file['bitrix_user']
            else:
                return 'None'
        else:
            self.create_json()
    
    def get_bitrix_password(self):
        if self.verify_if_json_exists():
            if self.json_file['bitrix_password']:
                return self.json_file['bitrix_password']
            else:
                return 'None'
        else:
            self.create_json()
    
    def get_forum_user(self):
        if self.verify_if_json_exists():
            if self.json_file['forum_user']:
                return self.json_file['forum_user']
            else:
                return 'None'
        else:
            self.create_json()
    
    def get_forum_password(self):
        if self.verify_if_json_exists():
            if self.json_file['forum_password']:
                return self.json_file['forum_password']
            else:
                return 'None'
        else:
            self.create_json()
    
    def set_username(self, username):
        self.json_setter('user', username)
    
    def set_password(self, password):
        self.json_setter('password', password)
    
    def set_host(self, host):
        self.json_setter('host', host)
            
    def set_port(self, port):
        self.json_setter('port', port)
    
    def set_database(self, database):
        self.json_setter('database', database)

    def set_bitrix_user(self, bitrix_user):
        self.json_setter('bitrix_user', bitrix_user)
    
    def set_bitrix_password(self, bitrix_password):
        self.json_setter('bitrix_password', bitrix_password)
        
    def set_forum_user(self, forum_user):
        self.json_setter('forum_user', forum_user)
    
    def set_forum_password(self, forum_password):
        self.json_setter('forum_password', forum_password)    
    
    def json_setter(self, key, value):
        if not self.verify_if_json_exists():
            self.create_json()
        self.json_file[key] = value
        self.write_json()
        
        if key == 'host':
            key = 'IPServidor'
        elif key == 'port':
            key = 'PortaServidor'
        if key != 'user' and key != 'password':
            self.ini_config.config_att_value(key, value)
        return 'sucess'

    def write_json(self):
        with open(self.path_json, 'w') as f:
            json.dump(self.json_file, f)
        return 'sucess'
    
    def verify_if_path_components_exist(self):
        if os.path.exists(r'components'):
            return True
        else:
            return False

    def create_components_path(self):
        if not self.verify_if_path_components_exist():
            os.mkdir(r'components')
        return 'sucess'

    def create_defaut_json(self):
        if not self.verify_if_json_exists():
            with open(self.path_json, 'w') as f:
                f.write(
                    """{"user": "default",
                    "password": "default",
                    "host": "localhost",
                    "port": "3306",
                    "database": "default",
                    "bitrix_user":"default",
                    "bitrix_password":"default",
                    "forum_user":"default",
                    "forum_password":"default"
                    }""")
        return 'sucess'
    
    def verify_if_images_path_exists(self):
        if os.path.exists(r'images'):
            return True
        else:
            return False
        
if __name__ == '__main__':

    f = File()
    print(f.read_json(database=True))
    # f.set_host('10.1.1.220')
    # print(f.username, f.password, f.host, f.port, f.database, f.json_file)
    # f.set_username('root')

import os
import sys
path = os.path.abspath('./')
sys.path.append(path)
import json
from components.ini_handle import IniConfig
from components.os_handle import OsHandler
import win32net
import win32file
from multiprocessing import freeze_support
from datetime import datetime
class File():
    def __init__(self):
        self.ini_config = IniConfig()
        self.path_json = r'components/params.json'
        self.path_log = r'components/log.txt'
        self.json_file = self.read_json()
        self.init_json_config_align_with_dotini()
        self.username = self.get_username()
        self.password = self.get_password()
        self.host = self.get_host()
        self.port = self.get_port()
        self.database = self.get_database()
        self.os_handler = OsHandler()
        self.remote_path_log = rf'\\192.168.2.244\shared\{self.os_handler.get_machine_name()}.txt'
        data = {
            'remote': r'\\192.168.2.244\shared', 
            'local': '',
            'username': 'administrador',
            'password': 'senha@123'
        }
        self.local_machine = False
        try:
            win32net.NetUseAdd(None, 2, data)
        except:
            self.local_machine = True
            print('maquinaLocal')
        
    
    def init_txt(self):
        if self.os_handler.verify_if_has_connection(log_path=True):

            if self.verify_if_path_exists(self.path_log) and self.verify_if_path_exists(self.remote_path_log):
                return True
            else:
                self.create_log_txt()
                return True
          
    def create_log_txt(self):
            if self.verify_if_path_exists(self.path_log) and self.verify_if_path_exists(self.remote_path_log):
                return True
            elif not self.verify_if_path_components_exist():
                self.create_components_path()
                return True
            else:
                data_list = self.os_handler.init_data_user()
                for item in data_list:
                    value = data_list.get(item)
                    self.log_write(item+ ': '+ str(value))
                    if self.os_handler.verify_if_has_connection(log_path = True):
                        if not self.local_machine:
                            self.write_to_file(self.remote_path_log, item+': '+str(value))
                        else:
                            self.log_write(item+ ': '+ str(value), remote=True)         
                return True
        
    def log_write(self, text, remote = False):
        actual_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        text = text+f'     || {actual_datetime}\n'
        if not remote:
            if not self.verify_if_path_components_exist():
                self.create_components_path()
                return True
            else:
                with open(self.path_log, 'a') as f:
                    f.write(text)
                return True
        else:
            if self.os_handler.verify_if_has_connection(log_path=True):
                with open(self.remote_path_log, 'a') as f:
                    f.write(text)
                return True
            else:   
                return False
    
    def add_new_logs(self, text):
        if self.verify_if_path_exists(self.path_log) and self.verify_if_path_exists(self.remote_path_log):
            self.log_write(text)
            if self.local_machine:
                self.log_write(text, remote=True)
            else:
                self.write_to_file(self.remote_path_log, text) 
        else:
            self.create_log_txt()

                
    def write_to_file(self, filename, text):
        actual_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Open the file or create it if it doesn't exist
        handle = win32file.CreateFile(
            filename,  # File name
            win32file.GENERIC_WRITE,  # Access type
            0,  # Share mode
            None,  # Security
            win32file.OPEN_ALWAYS,  # Disposition (create if it doesn't exist, open otherwise)
            0,  # File attributes
            None  # Template file
        )

        # Encode the string into bytes
        text = text+f'    || {actual_datetime}\n'
        text = text.encode()

        # Set the file pointer to the end of the file to append content
        win32file.SetFilePointer(handle, 0, win32file.FILE_END)

        # Write to the file
        win32file.WriteFile(handle, text)

        # Close the file
        win32file.CloseHandle(handle)
    
    def create_json(self):
        if self.verify_if_path_exists(self.path_json):
            return False
        elif not self.verify_if_path_components_exist():
            self.create_components_path()
            self.create_defaut_json()
            return True
        else:
            self.create_defaut_json()
            return True
        
    def verify_if_path_exists(self, path):
        if os.path.exists(path):
            return True
        else:
            return False

    def read_json(self, database = False):
        if self.verify_if_path_exists(self.path_json):
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
               
    def get_username(self):
        if self.verify_if_path_exists(self.path_json):
            if self.json_file['user']:
                return self.json_file['user']
            else:
                return 'None'
        else:
            self.create_json()
    
    def get_password(self):
        if self.verify_if_path_exists(self.path_json):
            if self.json_file['password']:
                return self.json_file['password']
            else:
                return 'None'
        else:
            self.create_json()
            
    def get_host(self):
        if self.verify_if_path_exists(self.path_json):
            if self.json_file['host']:
                return self.json_file['host']
            else:
                return 'None'
        else:
            self.create_json()
            
    def get_port(self):
        if self.verify_if_path_exists(self.path_json):
            if self.json_file['port']:
                return self.json_file['port']
            else:
                return 'None'
        else:
            self.create_json()
            
    def get_port(self):
        if self.verify_if_path_exists(self.path_json):
            if self.json_file['port']:
                return self.json_file['port']
            else:
                return 'None'
        else:
            self.create_json()
            
    def get_database(self):
        if self.verify_if_path_exists(self.path_json):
            if self.json_file['database']:
                return self.json_file['database']
            else:
                return 'None'
        else:
            self.create_json()
    
    def get_bitrix_user(self):
        if self.verify_if_path_exists(self.path_json):
            if self.json_file['bitrix_user']:
                return self.json_file['bitrix_user']
            else:
                return 'None'
        else:
            self.create_json()
    
    def get_bitrix_password(self):
        if self.verify_if_path_exists(self.path_json):
            if self.json_file['bitrix_password']:
                return self.json_file['bitrix_password']
            else:
                return 'None'
        else:
            self.create_json()
    
    def get_forum_user(self):
        if self.verify_if_path_exists(self.path_json):
            if self.json_file['forum_user']:
                return self.json_file['forum_user']
            else:
                return 'None'
        else:
            self.create_json()
    
    def get_forum_password(self):
        if self.verify_if_path_exists(self.path_json):
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
        if not self.verify_if_path_exists(self.path_json):
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
        if not self.verify_if_path_exists(self.path_json):
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
    # print(f.create_log_txt())
    f.add_new_logs('teste')
    
    # print(f.verify_if_path_exists(f.remote_path_log))
    # print(f.read_json(database=True))
    # f.set_host('10.1.1.220')
    # print(f.username, f.password, f.host, f.port, f.database, f.json_file)
    # f.set_username('root')

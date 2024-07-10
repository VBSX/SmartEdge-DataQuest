from os.path import (abspath as path_os, exists) 
from os import mkdir
from sys import path as syspath
path = path_os('./')
syspath.append(path)
from json import (load as read_json, dump as write_json)
from components.ini_handle import IniConfig
from components.os_handle import OsHandler
from win32net import NetUseAdd
from win32file import (
    CreateFile,
    WriteFile,
    CloseHandle,
    GENERIC_WRITE,
    FILE_END,
    SetFilePointer,
    OPEN_ALWAYS)

# from multiprocessing import freeze_support
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
        self.lost_connection = False
        self.local_machine = False
        if self.os_handler.verify_if_has_connection(log_path=True) == True:
            try:
                NetUseAdd(None, 2, data)
            except:
                self.local_machine = True
                print('maquinaLocal')
        else:
            self.lost_connection = True
        
    
    def init_txt(self):
        if self.os_handler.verify_if_has_connection(log_path=True):

            if self.verify_if_path_exists(self.path_log) and self.verify_if_path_exists(self.remote_path_log):
                return True
            else:
                self.create_log_txt()
                return True
          
    def create_log_txt(self):
            has_connection = self.os_handler.verify_if_has_connection(log_path=True)
            if self.verify_if_path_exists(self.path_log) and self.verify_if_path_exists(self.remote_path_log):
                return True
            elif not has_connection and self.verify_if_path_exists(self.path_log):
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
        if not self.lost_connection:
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
        handle = CreateFile(
            filename,  # File name
            GENERIC_WRITE,  # Access type
            0,  # Share mode
            None,  # Security
            OPEN_ALWAYS,  # Disposition (create if it doesn't exist, open otherwise)
            0,  # File attributes
            None  # Template file
        )

        # Encode the string into bytes
        text = text+f'    || {actual_datetime}\n'
        text = text.encode()

        # Set the file pointer to the end of the file to append content
        SetFilePointer(handle, 0, FILE_END)

        # Write to the file
        WriteFile(handle, text)

        # Close the file
        CloseHandle(handle)
    
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
        if exists(path):
            return True
        else:
            return False

    def read_json(self, database = False):
        if self.verify_if_path_exists(self.path_json):
                with open(self.path_json, 'r') as f:
                    content = read_json(f)
                if not database:
                    return content   
                else:
                    # retira os campos referente as credenciais do bitrix e forum
                    try:
                        content.pop('bitrix_user')
                        content.pop('bitrix_password')
                        content.pop('forum_user')
                        content.pop('forum_password')
                        content.pop('user_releaser')
                        content.pop('name_of_program')
                        content.pop('test_mode')
                    except:
                        print('erro ao retirar os campos referente as credenciais do bitrix e forum')
                    return content
                
        else:
            self.create_json()
            with open(self.path_json, 'r') as f:
                content = read_json(f)
                return content
    
    def init_json_config_align_with_dotini(self):
            host = self.ini_config.host_ini
            database = self.ini_config.database_ini
            port = self.ini_config.port_ini
            test_mode = self.ini_config.test_mode
            self.set_database(database)
            self.set_host(host)
            self.set_port(port)
            self.set_test_mode(test_mode)
                  
    def get_username(self):
        return self.get_info_json('user')
    
    def get_password(self):
        return self.get_info_json('password')
            
    def get_host(self):
        return self.get_info_json('host')
            
    def get_port(self):
        return self.get_info_json('port')
            
    def get_database(self):
        return self.get_info_json('database')
    
    def get_bitrix_user(self):
        return self.get_info_json('bitrix_user')
    
    def get_bitrix_password(self):
        return self.get_info_json('bitrix_password')
    
    def get_forum_user(self):
        return self.get_info_json('forum_user')
    
    def get_forum_password(self):
        return self.get_info_json('forum_password')
    
    def get_user_releaser(self):
        return self.get_info_json('user_releaser')
    
    def get_program_name(self):
        return self.get_info_json('name_of_program')

    def get_test_mode(self):
        return self.get_info_json('test_mode')
    
    def get_info_json(self, field):
        if self.verify_if_path_exists(self.path_json):
            campo = self.json_file[field]  
            if campo or campo == '' or campo >=0:
                return campo
            else:
                return 'None'
        else:
            self.create_json()
            self.get_info_json(field)
    
    def set_test_mode(self, test_mode):
        self.json_setter('test_mode', test_mode)
    
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
    
    def set_user_releaser(self, user_releaser):
        self.json_setter('user_releaser', user_releaser)
    
    def set_name_of_program(self, name_of_program):
        self.json_setter('name_of_program', name_of_program)
    
    def json_setter(self, key, value):
        if not self.verify_if_path_exists(self.path_json):
            self.create_json()
        self.json_file[key] = value
        self.write_json()
        
        if key == 'host':
            key = 'IPServidor'
        elif key == 'port':
            key = 'PortaServidor'
        elif key == 'test_mode':
            self.ini_config.set_test_mode(f"{value}")
        if key != 'user' and key != 'password':
            self.ini_config.config_att_value(key, value)
        return 'sucess'

    def write_json(self):
        with open(self.path_json, 'w') as f:
            write_json(self.json_file, f)
        return 'sucess'
    
    def verify_if_path_components_exist(self):
        if exists(r'components'):
            return True
        else:
            return False

    def create_components_path(self):
        if not self.verify_if_path_components_exist():
            mkdir(r'components')
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
                    "forum_password":"default",
                    "user_releaser":"default",
                    "name_of_program":"default",
                    "test_mode":1
                    }""")
        return 'sucess'
    
    def verify_if_images_path_exists(self):
        if exists(r'images'):
            return True
        else:
            return False
            
if __name__ == '__main__':
    f = File()
    # print(f.create_log_txt())
    print(f.get_test_mode())
    print(f.add_new_logs('asdas'))
    # f.set_test_mode(0)
    
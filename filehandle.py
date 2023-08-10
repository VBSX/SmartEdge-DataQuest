import os
import json

class File():
    def __init__(self):
        self.json_file = self.read_json()
        self.username = self.get_username()
        self.password = self.get_password()
        self.host = self.get_host()
        self.port = self.get_port()
        self.database = self.get_database()
    
    def create_json(self):
        if self.verify_if_json_exists():
            return False
        else:
            with open('params.json', 'w') as f:
                f.write('{}')
                return True
        
    def verify_if_json_exists(self):
        file_name = 'params.json'
        if os.path.exists(file_name):
            return True
        else:
            return False
    
    def read_json(self):
        if self.verify_if_json_exists():
            with open('params.json', 'r') as f:
                content = json.load(f)
                return content
        else:
            self.create_json()
                
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
    
    def set_username(self, username):
        if not self.verify_if_json_exists():
            self.create_json()
        self.json_file['user'] = username
        self.write_json()
        return 'sucess'
    
    def set_password(self, password):
        if not self.verify_if_json_exists():
            self.create_json()
        self.json_file['password'] = password
        self.write_json()
        return 'sucess'
    
    def set_host(self, host):
        if not self.verify_if_json_exists():
            self.create_json()
        self.json_file['host'] = host
        self.write_json()
        return 'sucess'
            
    def set_port(self, port):
        if not self.verify_if_json_exists():
            self.create_json()
        self.json_file['port'] = port
        self.write_json()
        return 'sucess'
    
    def set_database(self, database):
        if not self.verify_if_json_exists():
            self.create_json()
            
        self.json_file['database'] = database
        self.write_json()
        return 'sucess'

    
    def write_json(self):
        with open('params.json', 'w') as f:
            json.dump(self.json_file, f)
        return 'sucess'
    
        
if __name__ == '__main__':
    
    f = File()
    print(f.username, f.password, f.host, f.port, f.database, f.json_file)
    # f.set_username('root')

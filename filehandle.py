import os
class File():
    def __init__(self) -> None:
        pass
    
    def create_json(self, data):
        if self.verify_if_json_exists():
            return False
        else:
            with open('params.json', 'w') as f:
                f.write(data)
                return True
        
    def verify_if_json_exists(self):
        file_name = 'params.json'
        if os.path.exists(file_name):
            return True
        else:
            return False
    
    def read_json(self):
        with open('params.json', 'r') as f:
            return f.read()
        
if __name__ == '__main__':
    
    File = File()
    print(File.verify_if_json_exists())
    create_json = File.create_json('{"teste":"teste"}')
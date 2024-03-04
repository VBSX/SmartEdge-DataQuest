from os.path import abspath as path_os
from sys import path as syspath
path = path_os('./')
syspath.append(path)
from cryptography.fernet import Fernet
from base64 import urlsafe_b64decode, urlsafe_b64encode
from components.filehandle import File

class Cripter(Fernet):
    def __init__(self):
        self.key = b'nPwQhXeEkt3A7DC4ZqtdVl2xzYQe6IHoq3kmztTIx1M='
        self.file_handler = File()
    def decrypt(self, password):
        try:
            # Decodifica a string base64
            encrypted_bytes = urlsafe_b64decode(password)

            # Cria um objeto Fernet com a chave e descriptografa
            cipher = Fernet(self.key)
            decrypted_text = cipher.decrypt(encrypted_bytes).decode('utf-8')
            return decrypted_text
        except Exception as e:
            self.file_handler.add_new_logs(f"Erro ao descriptografar: {e}")
            print(f"Erro ao descriptografar: {e}")
            return None
        
    def encrypt(self, password):
        # Cria um objeto Fernet com a chave
        cipher = Fernet(self.key)

        # Criptografa o texto e codifica para base64
        encrypted_bytes = cipher.encrypt(password.encode('utf-8'))
        encrypted_text = urlsafe_b64encode(encrypted_bytes).decode('utf-8')
        return encrypted_text
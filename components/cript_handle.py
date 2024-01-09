from cryptography.fernet import Fernet
import base64

class Cripter(Fernet):
    def __init__(self):
        self.key = b'nPwQhXeEkt3A7DC4ZqtdVl2xzYQe6IHoq3kmztTIx1M='
        
    def decrypt(self, password):
        try:
            # Decodifica a string base64
            encrypted_bytes = base64.urlsafe_b64decode(password)

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
        encrypted_text = base64.urlsafe_b64encode(encrypted_bytes).decode('utf-8')
        return encrypted_text
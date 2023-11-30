from cryptography.fernet import Fernet

def generate_key():
    # Gera uma chave aleatória
    return Fernet.generate_key()

def encrypt_text(key, text):
    # Cria um objeto Fernet com a chave
    cipher = Fernet(b'nPwQhXeEkt3A7DC4ZqtdVl2xzYQe6IHoq3kmztTIx1M=')
    # Criptografa o texto
    encrypted_text = cipher.encrypt(text.encode('utf-8'))
    return encrypted_text

def decrypt_text(key, encrypted_text):
    # Cria um objeto Fernet com a chave
    cipher = Fernet(key)
    # Descriptografa o texto
    decrypted_text = cipher.decrypt(encrypted_text).decode('utf-8')
    return decrypted_text

# Exemplo de uso:
message = "teste"

# Gera uma chave
key = generate_key()
print(f"Key: {key}")

# Criptografa a mensagem
encrypted_message = encrypt_text(key, message)
print(f"Encrypted Message: {encrypted_message}")

# Descriptografa a mensagem
decrypted_message = decrypt_text(b'nPwQhXeEkt3A7DC4ZqtdVl2xzYQe6IHoq3kmztTIx1M=', encrypted_message)
print(f"Decrypted Message: {decrypted_message}")

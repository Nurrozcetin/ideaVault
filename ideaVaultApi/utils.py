from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def save_key(key, filename):
    with open(filename, 'wb') as key_file:
        key_file.write(key)

def load_key(filename):
    with open(filename, 'rb') as key_file:
        return key_file.read()

def encrypt_message(message, key):
    f = Fernet(key)
    if isinstance(message, str):
        message = message.encode()  
    encrypted_message = f.encrypt(message)
    return encrypted_message

def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    if isinstance(encrypted_message, str):
        encrypted_message = encrypted_message.encode()  
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message

from cryptography.fernet import Fernet

# Anahtar üretimi
def generate_key():
    return Fernet.generate_key()

# Anahtarı dosyaya kaydetme
def save_key(key, filename):
    with open(filename, 'wb') as key_file:
        key_file.write(key)

# Anahtarı dosyadan okuma
def load_key(filename):
    with open(filename, 'rb') as key_file:
        return key_file.read()

# Şifreleme
def encrypt_message(message, key):
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

# Şifre çözme
def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message

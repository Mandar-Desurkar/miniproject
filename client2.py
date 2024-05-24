import socket
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import random

def quantum_encrypt(data):
    return str(random.randint(10000, 99999))

def encrypt(data, encryption_level, key=None):
    if encryption_level == '1':
        return data
    elif encryption_level == '2':
        cipher = AES.new(base64.b64decode(key), AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext = cipher.encrypt(data.encode())
        return base64.b64encode(nonce + ciphertext).decode('utf-8')
    elif encryption_level == '3':
        otp = quantum_encrypt(data)
        print(f"OTP to decrypt the data: {otp}")
        return otp

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 65432))

while True:
    encryption_level = input("Enter encryption level (1- No Encryption, 2- AES Encryption, 3- Quantum Encryption) or 'exit' to quit: ")
    if encryption_level == 'exit':
        client_socket.send(encryption_level.encode())
        break

    client_socket.send(encryption_level.encode())

    key = None
    if encryption_level == '2':
        key = base64.b64encode(get_random_bytes(16)).decode('utf-8')
        client_socket.send(key.encode())

    otp = None
    if encryption_level == '3':
        otp = quantum_encrypt(None)
        print(f"Generated OTP for the server: {otp}")

    data = input("Enter the data to send or 'exit' to quit: ")
    if data == 'exit':
        client_socket.send(data.encode())
        break

    encrypted_data = encrypt(data, encryption_level, key)
    client_socket.send(encrypted_data.encode())

client_socket.close()

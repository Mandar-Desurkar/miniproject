import socket
from Crypto.Cipher import AES
import base64
import Protocols

ALICE_ADDR = 'localhost'
BOB_ADDR = 'localhost'
ALICE_PORT = 4000
BOB_PORT = 8000

def receive_message_normal():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((ALICE_ADDR, ALICE_PORT))
        server_socket.listen(1)
        conn, addr = server_socket.accept()
        with conn:
            data = conn.recv(1024).decode()
            print(f"Received message: {data}")

def receive_message_aes(key):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        print('hi1')
        server_socket.bind((ALICE_ADDR, ALICE_PORT))
        server_socket.listen(1)
        print('ko2')
        try:
            conn, addr = server_socket.accept()
        except:
            print('connection')
        with conn:
            print('ko')
            encrypted_data = conn.recv(1024)
            nonce = encrypted_data[:16]
            print('hi2')
            tag = encrypted_data[16:32]
            ciphertext = encrypted_data[32:]

            cipher = AES.new(key.encode(), AES.MODE_EAX, nonce=nonce)
            print('hi3')

            decrypted_data = cipher.decrypt_and_verify(ciphertext, tag).decode()
            print(f"Decrypted message: {decrypted_data}")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    server_socket.bind(('localhost', 8000))
    server_socket.listen(1)
    print("Server listening on port 8000...")

    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    choice = conn.recv(1024).decode()
    choice='2'

    if choice == '1':
        receive_message_normal()
    elif choice == '2':
        print('hi')
        receive_message_aes('asdfasdfasdfasdf')
    elif choice == '3':
        Protocols.receive_a_qmail(BOB_PORT, ALICE_ADDR, ALICE_PORT)
    else:
        print("Invalid choice. Exiting.")
        return

if __name__ == "__main__":
    main()

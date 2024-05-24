import socket
from Crypto.Cipher import AES
import base64
import Protocols

ALICE_ADDR = 'localhost'
BOB_ADDR = 'localhost'
ALICE_PORT = 6000
BOB_PORT = 7000

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
        server_socket.bind((ALICE_ADDR, ALICE_PORT))
        server_socket.listen(1)
        conn, addr = server_socket.accept()
        with conn:
            encrypted_data = conn.recv(1024)
            nonce = encrypted_data[:16]
            tag = encrypted_data[16:32]
            ciphertext = encrypted_data[32:]

            cipher = AES.new(key.encode(), AES.MODE_EAX, nonce=nonce)
            decrypted_data = cipher.decrypt_and_verify(ciphertext, tag).decode()
            print(f"Decrypted message: {decrypted_data}")

def main():
    print("Choose the decryption method:")
    print("1. Normal (no decryption)")
    print("2. AES decryption")
    print("3. Quantum decryption (using protocols)")

    choice = input("Enter your choice (1/2/3): ")

    if choice == '1':
        receive_message_normal()
    elif choice == '2':
        key = input("Enter AES decryption key (16 bytes): ")
        receive_message_aes(key)
    elif choice == '3':
        Protocols.receive_a_qmail(BOB_PORT, ALICE_ADDR, ALICE_PORT)
    else:
        print("Invalid choice. Exiting.")
        return

if __name__ == "__main__":
    main()

import socket
from Crypto.Cipher import AES
import base64
import pickle
import Protocols

ALICE_ADDR = 'localhost'
BOB_ADDR = 'localhost'
ALICE_PORT = 4000
BOB_PORT = 8000


def send_message_normal(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((BOB_ADDR, BOB_PORT))
        client_socket.sendall(message.encode())


def send_message_aes(message, key):
    cipher = AES.new(key.encode(), AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((BOB_ADDR, BOB_PORT))
        client_socket.sendall(base64.b64encode(cipher.nonce + tag + ciphertext))


def main():
    message = input("Enter the message to send: ")

    print("Choose the encryption method:")
    print("1. Normal (no encryption)")
    print("2. AES encryption")
    print("3. Quantum encryption (using protocols)")

    choice = input("Enter your choice (1/2/3): ")
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    #      client_socket.send(choice.encode())

    if choice == '1':
        send_message_normal(message)
    elif choice == '2':
        send_message_aes(message, 'asdfasdfasdfasdf')
    elif choice == '3':
        otp = input("Enter the OTP for quantum encryption (1 or 0): ")
        Protocols.send_a_qmail(message, ALICE_PORT, BOB_ADDR, BOB_PORT)
    else:
        print("Invalid choice. Exiting.")
        return


if __name__ == "__main__":
    main()

import socket
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer, AerSimulator

def quantum_decrypt(otp):
    simulator = AerSimulator()
    circuit = QuantumCircuit(1, 1)
    if otp == '1':
        circuit.x(0)
    circuit.measure([0], [0])
    compiled_circuit = transpile(circuit, simulator)
    result = simulator.run(compiled_circuit, shots=1).result()
    counts = result.get_counts(circuit)
    return '1' if '1' in counts else '0'

def decrypt(data, encryption_level, key=None, otp=None):
    if encryption_level == '1':
        return data
    elif encryption_level == '2':
        data = base64.b64decode(data)
        nonce = data[:16]
        ciphertext = data[16:]
        cipher = AES.new(base64.b64decode(key), AES.MODE_EAX, nonce=nonce)
        return cipher.decrypt(ciphertext).decode('utf-8')
    elif encryption_level == '3':
        return quantum_decrypt(otp)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 65432))
server_socket.listen(1)
print("Server listening on port 65432...")

conn, addr = server_socket.accept()
print(f"Connected by {addr}")

encryption_level = conn.recv(1024).decode()
key = None
if encryption_level == '2':
    t=conn.recv(1024)
    print(t)
    key = t.decode()


otp = None
if encryption_level == '3':
    otp = input("Enter the OTP provided by the client: ")

data = conn.recv(1024).decode()

decrypted_data = decrypt(data, encryption_level, key, otp)
print(f"Decrypted data: {decrypted_data}")

conn.close()
server_socket.close()

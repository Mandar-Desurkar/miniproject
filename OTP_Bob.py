from SocketChannel2 import SocketChannel
import Protocols
import pickle
import socket

ALICE_ADDR = 'localhost'
BOB_ADDR = 'localhost'
ALICE_PORT = 6000
BOB_PORT = 7000

def main():

  Protocols.receive_a_qmail(BOB_PORT, ALICE_ADDR, ALICE_PORT, adversary=False)

  pass

if __name__ == "__main__":
  main()
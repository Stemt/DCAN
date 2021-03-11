import socket
import os
from _thread import *

import Database_interface as db

HOST = '0.0.0.0'
PORT = 1233

ServerSocket =  socket.socket()
ThreadCount = 0
running = True


try:
    ServerSocket.bind((HOST,PORT))
except socket.error as e:
    print(str(e))

print('server has started, waiting for connection...')
ServerSocket.listen();

while True:
    Client, address = ServerSocket.accept()
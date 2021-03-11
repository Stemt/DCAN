import socket
import os
from _thread import *
from TCPSession import TCPSession

import Database_interface as db

HOST = '0.0.0.0'
PORT = 1233

sslContext = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
threadCount = 0
running = True

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as socket:

    try:
        socket.bind((HOST,PORT))
    except socket.error as e:
        print(str(e))

    print('server has started, waiting for connection...')
    socket.listen(5);

    with sslContext.wrap_socket(socket, server_side=True) as sslSocket:
        while True:
            connection = sslSocket.accept()
            start_new_thread(TCPSession,connection)
            threadCount += 1
            print('new connection accepted\ntotal connections: ' + str(threadCount))

    socket.close()
            

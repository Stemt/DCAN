import json
import bcrypt

class TCPSession:
    def __init__(self,connection,address):
        self.connection = connection
        self.address = address
        self.running = True

    def run(self):
        while self.running:
            data = self.connection.recv(4096)
            parsedData = json.loads(data)

    def authorize(username,password):
        bcrypt.hashpw(password.encode(),)
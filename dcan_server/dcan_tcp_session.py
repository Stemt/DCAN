import json
import bcrypt

import Database_interface as db

class TCPSession:
    def __init__(self,client,address):
        self.client = client
        self.address = address
        self.running = True
        self.run()

    def run(self):
        while self.running:
            data = self.connection.recv(4096)
            parsedData = json.loads(data)
            if(parsedData['message_type'] == "")

    def authorize(username,password):
        db.verify_user(username,password)


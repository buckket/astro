import socket
import uuid

import msgpack


class AstroUDPClient(object):

    def __init__(self, host, port, key):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(1.0)

        self.uuid = str(uuid.uuid4())

        self.host = host
        self.port = port
        self.key = key

    def send(self, data):
        data['key'] = self.key
        data['uuid'] = self.uuid
        data_packed = msgpack.packb(data)
        self.socket.sendto(data_packed + '\n', (self.host, self.port))
        success = self.receive()
        try:
            if success['message'] == 'data received':
                return True
            else:
                return False
        except:
            return False

    def receive(self):
        try:
            data_packed = self.socket.recv(1024).strip()
        except socket.timeout:
            return None
        data = msgpack.unpackb(data_packed)
        if data['key'] == self.key and data['uuid'] == self.uuid:
            return data
        else:
            return None

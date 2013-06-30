from astro.client.udp import AstroUDPClient


class BaseDispatcher(object):

    def __init__(self, host, port, key):
        self.host = host
        self.port = port
        self.key = key

    def generate_socket(self):
        return AstroUDPClient(host=self.host, port=self.port, key=self.key)

    def wrap_data(self, task, command, args):
        return {'task': task, 'command': command, 'args': args}

    def try_send(self, socket, data):
        if not socket.send(data):
            print 'Failed to send command'
            return False
        else:
            print "Successfully send command"
            return True

    def try_catch_response(self, socket):
        data = socket.receive()
        if data:
            return data
        else:
            print "No answer received"
            return False

    def do(self, args):
        pass

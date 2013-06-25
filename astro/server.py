import SocketServer
import msgpack
import logging


class AstroUDPServer(SocketServer.UDPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, key=None, temp=None, radio=None, light=None):
        SocketServer.UDPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate=True)
        self.key = key
        self.temp = temp
        self.radio = radio
        self.light = light

        self.logger = logging.getLogger('astro.server')


class AstroUDPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        logger = self.server.logger
        raw_data = self.request[0].strip()
        socket = self.request[1]
        secret_key = self.server.key

        data = None
        try:
            data = msgpack.unpackb(raw_data)
        except (msgpack.exceptions.UnpackException, AttributeError, EOFError, ImportError, IndexError):
            logger.error('UnpackingError (%s)', self.client_address[0])

        if data:

            task = data.get('task', None)
            command = data.get('command', None)
            args = data.get('args', None)
            uuid = data.get('uuid', None)
            key = data.get('key', None)

            if key ==  secret_key:

                def answer(code=0, message=None):
                    data = {'code': code, 'message': message, 'uuid': uuid, 'key': key}
                    logger.debug('Answering %s: %s', self.client_address, data)
                    socket.sendto(msgpack.packb(data) + '\n', self.client_address)

                logger.info('Received command from %s: (%s, %s)', self.client_address[0], task, command)
                logger.debug('task: %s, command: %s,  args: %s', task, command, args)

                answer(0, 'data received')

                if task == 'radio':
                    self.server.radio.queue.put(((command, args), answer))
                elif task == 'temp':
                    self.server.temp.queue.put(((command, args), answer))
                elif task == 'light':
                    self.server.light.queue.put(((command, args), answer))
                else:
                    logger.warn('invalid task: %s', task)
                    answer(1, 'invalid task')

            else:
                logger.warn('Received command from %s with invalid key', self.client_address[0])

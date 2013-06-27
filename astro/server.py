import SocketServer
import logging

import msgpack


class AstroUDPServer(SocketServer.UDPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, key=None):
        SocketServer.UDPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate=True)

        self.key = key
        self.handler = {}

        self.logger = logging.getLogger('astro.server')

    def add_handler(self, ref, name):
        if name in self.handler:
            self.logger.warn('%s is already a registered handler, skipping')
        else:
            self.handler[name] = ref
            self.logger.info('Registered new handler: %s' % name)


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

            if key == secret_key:

                def answer(code=0, message=None):
                    data = {'code': code, 'message': message, 'uuid': uuid, 'key': key}
                    logger.debug('Answering %s: %s', self.client_address, data)
                    socket.sendto(msgpack.packb(data) + '\n', self.client_address)

                logger.info('Received command from %s: (%s, %s)', self.client_address[0], task, command)
                logger.debug('task: %s, command: %s,  args: %s', task, command, args)

                answer(0, 'data received')

                try:
                    self.server.handler[task].queue.put(((command, args), answer))
                except KeyError:
                    logger.warn('invalid task: %s', task)
                    answer(1, 'invalid task')

            else:
                logger.warn('Received command from %s with invalid key', self.client_address[0])

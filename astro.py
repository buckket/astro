#!/usr/bin/env python

import SocketServer

import logging
import pickle

from ConfigParser import SafeConfigParser

from controller.temp import TempController
from controller.radio import RadioController
from controller.light import LightController


class UDPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        raw_data = self.request[0].strip()
        socket = self.request[1]

        data = None
        try:
            data = pickle.loads(raw_data)
        except (pickle.UnpicklingError, AttributeError, EOFError, ImportError, IndexError):
            logger.error('UnpicklingError (%s)', self.client_address[0])

        if data:

            task = data.get('task', None)
            command = data.get('command', None)
            args = data.get('args', None)
            uuid = data.get('uuid', None)
            key = data.get('key', None)

            if key ==  cfg.get('network', 'key'):

                def answer(code=0, message=None):
                    data = {'code': code, 'message': message, 'uuid': uuid, 'key': key}
                    logger.debug('Answering %s: %s', self.client_address, data)
                    socket.sendto(pickle.dumps(data) + '\n', self.client_address)

                logger.info('Received command from %s: (%s, %s)', self.client_address[0], task, command)
                logger.debug('task: %s, command: %s,  args: %s', task, command, args)

                answer(0, 'data received')

                if task == 'radio':
                    radio.queue.put(((command, args), answer))
                elif task == 'temp':
                    temp.queue.put(((command, args), answer))
                elif task == 'light':
                    light.queue.put(((command, args), answer))
                else:
                    answer(1, 'invalid task')

            else:
                logger.warn('Received command from %s with invalid key', self.client_address[0])


def setup_logger():
    logger = logging.getLogger('astro')
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler('astro.log')
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s : %(name)-11s : %(levelname)-8s : %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

def setup_config():
    parser = SafeConfigParser()
    parser.read('astro.cfg')
    return parser


if __name__ == "__main__":
    logger = setup_logger()
    logger.info('Astro is starting')

    logger.info('Reading configuration')
    cfg = setup_config()

    host = cfg.get('network', 'host')
    port = cfg.getint('network', 'port')
    server = SocketServer.UDPServer((host, port), UDPHandler)
    logger.info('Socket bound to %s:%i', host, port)

    logger.info('Initializing TempController')
    w1_device = cfg.get('temp', 'w1_device')
    xivley = {'apikey': cfg.get('temp', 'xivley_key'), 'url': cfg.get('temp', 'xivley_url')}
    period = cfg.getfloat('temp', 'period')
    temp = TempController(w1_device=w1_device, xivley=xivley, period=period)

    logger.info('Initializing RadioController')
    radio = RadioController()

    logger.info('Initializing LightController')
    red = cfg.get('light', 'red')
    green = cfg.get('light', 'green')
    blue = cfg.get('light', 'blue')
    frequency = cfg.getint('light', 'frequency')
    light = LightController(red=red, green=green, blue=blue, frequency=frequency)

    try:
        logger.info('Starting TempController')
        temp.start()
        logger.info('Starting RadioController')
        radio.start()
        logger.info('Starting LightController')
        light.start()
        logger.info('Starting UDPServer')
        server.serve_forever()

    except KeyboardInterrupt:
        logger.info('Astro is shutting down, bye! <3')
        temp.shutdown()
        radio.shutdown()
        light.shutdown()
        server.shutdown()

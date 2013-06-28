#!/usr/bin/env python

from astro.server.logger import setup_logger

from astro.server.config import setup_config
from astro.server.config import temp_config_helper
from astro.server.config import light_config_helper
from astro.server.config import server_config_helper

from astro.server.udp import AstroUDPServer, AstroUDPHandler

from astro.server.controller.temp import TempController
from astro.server.controller.radio import RadioController
from astro.server.controller.light import LightController


def main():
    logger = setup_logger()
    logger.info('Astro is starting')

    logger.info('Reading configuration')
    cfg = setup_config()

    if not cfg:
        logger.error('Config file not found or not readable')
        return

    logger.info('Initializing TempController')
    temp = TempController(**temp_config_helper(cfg))

    logger.info('Initializing RadioController')
    radio = RadioController()

    logger.info('Initializing LightController')
    light = LightController(**light_config_helper(cfg))

    logger.info('Initializing UDPServer')
    server_config = server_config_helper(cfg)
    server = AstroUDPServer((server_config['host'], server_config['port']), AstroUDPHandler, key=server_config['key'])
    server.add_handler(temp, 'temp')
    server.add_handler(radio, 'radio')
    server.add_handler(light, 'light')
    logger.info('Socket bound to %s:%i', server_config['host'], server_config['port'])

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

if __name__ == "__main__":
    main()

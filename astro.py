#!/usr/bin/env python

from astro.logger import setup_logger
from astro.config import setup_config

from astro.server import AstroUDPServer, AstroUDPHandler

from astro.controller.temp import TempController
from astro.controller.radio import RadioController
from astro.controller.light import LightController


def main():
    logger = setup_logger()
    logger.info('Astro is starting')

    logger.info('Reading configuration')
    cfg = setup_config()

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

    logger.info('Initializing AstroUDPServer')
    host = cfg.get('network', 'host')
    port = cfg.getint('network', 'port')
    key = cfg.get('network', 'key')
    server = AstroUDPServer((host, port), AstroUDPHandler, key=key, temp=temp, radio=radio, light=light)
    logger.info('Socket bound to %s:%i', host, port)

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

#!/usr/bin/env python

import argparse

from astro.server.main import AstroServer
from astro.client.main import AstroClient


def main():

    parser = argparse.ArgumentParser(description='Schaltpult MK I')
    parser.add_argument('-c', '--config',
        type=argparse.FileType('r'),
        dest='config_file',
        default='astro.cfg')

    subparsers = parser.add_subparsers(dest='command')

    # SERVER
    parser_server = subparsers.add_parser('server')

    # TEMP
    parser_temp = subparsers.add_parser('temp')
    parser_temp.add_argument('command_temp', nargs='?', default='get_temp')

    # LIGHT
    parser_light = subparsers.add_parser('light')
    parser_light.add_argument('command_light')
    parser_light.add_argument('r', type=int, nargs='?', default=0)
    parser_light.add_argument('b', type=int, nargs='?', default=0)
    parser_light.add_argument('g', type=int, nargs='?', default=0)

    # RADIO
    parser_radio = subparsers.add_parser('radio')
    parser_radio.add_argument('devices')
    parser_radio.add_argument('status')

    args = parser.parse_args()

    if args.command == 'server':
        server = AstroServer(config_file=args.config_file)
        server.start()
    elif args.command in ('temp', 'light', 'radio'):
        client = AstroClient(config_file=args.config_file)
        client.dispatch(args)

if __name__ == "__main__":
    main()

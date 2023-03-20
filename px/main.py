#!/usr/bin/env python3

# BoBoBo

import asyncio
import argparse
from .http_server import start_server, stop_server
from . import context as pxctx


def parse_args():
    """
    Parses command line arguments for starting the Px server.

    :return: An argparse.Namespace object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(description='Start a Px server.')

    parser.add_argument('-P', '--port', type=int, dest='port', default=8080,
                        help='Port to listen on')
    parser.add_argument('-H', '--host', dest='host', default='localhost',
                        help='Host to listen on')
    parser.add_argument('-c', '--conf', dest='conf_path', default=None,
                        help='Px yaml config file')

    # The parameters --http and --wsgi are mutually exclusive,
    # meaning only one of them can be used at a time.
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--http', dest='request_process_module',
                       help='module to handle HTTP requests')
    group.add_argument('--wsgi', dest='wsgi_app_module',
                       help='module to run a WSGI application')

    args = parser.parse_args()

    return args


def bootstrap(args):
    """
    Bootstrap the Px server with the given arguments.

    :param args: An argparse.Namespace object containing the parsed arguments.
    """
    if args.request_process_module:
        pxctx.setup_request_process_module(args.request_process_module)
    elif args.wsgi_app_module:
        pxctx.setup_wsgi_process_module(args.wsgi_app_module)
    else:
        pxctx.setup_default_process_module()

    asyncio.run(start_server(args.host, args.port,
                             pxctx.PxContext.request_process_module))


def main():
    """
    The main entry point for starting the Px server.
    """
    try:
        args = parse_args()
        print(f'Bootstrap Px Server with args: {args}')
        bootstrap(args)
    except Exception as e:
        print(f'Error starting server: {e}')
        asyncio.run(stop_server())


if __name__ == '__main__':
    main()

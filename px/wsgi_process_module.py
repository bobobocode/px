#!/usr/bin/env python3

# BoBoBo

import io
import sys
from .context import PxContext
from functools import reduce


async def filter_request_line(request_line):
    pass


async def filter_headers(headers):
    pass


async def filter_response(response):
    return response


async def dispatch(request_line, headers, body):
    """
    Dispatch http request by WSGI
    """
    environ = parse_request_environ(request_line, headers, body)
    resp = {}

    def start_response(status, response_headers):
        nonlocal resp
        resp['status'] = status
        resp['headers'] = {hd[0]: hd[1] for hd in response_headers}

    wsgi_app = PxContext.wsgi_app
    if wsgi_app:
        res = wsgi_app(environ, start_response)
        resp['body'] = reduce(lambda x, y: x + y, res)
        return resp
    else:
        raise Exception('No setup WSGI app in server context.')


def parse_request_environ(request_line, headers, body=b''):
    """
    Parses the request environment from the given request line, headers, and body.

    Args:
        request_line (tuple): A tuple containing the HTTP method, path, and version.
        headers (dict): A dictionary containing the HTTP headers.
        body (bytes): An optional bytes object representing the request body.

    Returns:
        dict: A dictionary representing the request environment.
    """
    method, path, version = request_line
    path_info, _, query_string = path.partition('?')
    content_type = headers.get('Content-Type', '')
    content_length = headers.get('Content-Length', '')

    environ = {
        'REQUEST_METHOD': method,
        'SCRIPT_NAME': '',
        'PATH_INFO': path_info,
        'QUERY_STRING': query_string,
        'SERVER_NAME': '',
        'SERVER_PORT': '',
        'SERVER_PROTOCOL': version,
        'CONTENT_TYPE': content_type,
        'CONTENT_LENGTH': content_length,
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'http',
        'wsgi.input': io.BytesIO(body),
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
    }

    for key, value in headers.items():
        key = key.upper().replace('-', '_')
        value = value.strip()
        if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            key = 'HTTP_' + key
        environ[key] = value

    return environ

#!/usr/bin/env python3

# BoBoBo


def wsgi_app():
    # do some process, like building app context
    # ...

    def _app(environ, start_response):
        """Simplest wsgi app."""
        params = environ['QUERY_STRING']
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        return ['Hello World!\n'.encode('utf-8'),
                ('QUERY_STRING:' + params).encode('utf-8')]

    return _app

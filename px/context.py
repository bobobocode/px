#!/usr/bin/env python3

# BoBoBo

import importlib


class ServerContext:
    """
    Class to hold server context data.
    """
    def __init__(self):
        self._data = {}

    @property
    def request_process_module(self):
        """
        Get the request processing module.
        """
        return self._data.get('request_process_module')

    @request_process_module.setter
    def request_process_module(self, value):
        """
        Set the request processing module.
        """
        self._data['request_process_module'] = value

    @property
    def wsgi_app(self):
        """
        Get the WSGI application.
        """
        return self._data.get('wsgi_app')

    @wsgi_app.setter
    def wsgi_app(self, value):
        """
        Set the WSGI application.
        """
        self._data['wsgi_app'] = value

    @property
    def logger(self):
        """
        Get the logger.
        """
        return self._data.get('logger')

    @logger.setter
    def logger(self, value):
        """
        Set the logger.
        """
        self._data['logger'] = value


PxContext = ServerContext()


def setup_default_process_module():
    """
    Set the default request processing module.
    """
    global PxContext
    from .example import request_process_module as m
    PxContext.request_process_module = m


def setup_request_process_module(request_process_module):
    """
    Set the request processing module from the given module name.
    """
    global PxContext
    try:
        m = importlib.import_module(request_process_module)
        PxContext.request_process_module = m
    except ImportError:
        raise ValueError('Could not import module %s.' % request_process_module)


def setup_wsgi_process_module(wsgi_app_module):
    """
    Set the WSGI application from the given module name.
    """
    global PxContext
    try:
        app_m = importlib.import_module(wsgi_app_module)
        if not hasattr(app_m, 'wsgi_app'):
            raise ValueError('Module %s does not have a wsgi_app function.' % wsgi_app_module)

        app = app_m.wsgi_app()
        PxContext.wsgi_app = app

        from . import wsgi_process_module as m
        PxContext.request_process_module = m
    except ImportError:
        raise ValueError('Could not import module %s.' % wsgi_app_module)

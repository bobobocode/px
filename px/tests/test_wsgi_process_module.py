#!/usr/bin/env python3
# BoBoBo
import asyncio
import sys
import unittest

from px.context import PxContext
from px.wsgi_process_module import dispatch
from px.wsgi_process_module import parse_request_environ


def wsgi_app():
    # do some process, like building app context
    # ...

    def _app(environ, start_response):
        """Simplest wsgi app."""
        params = environ["QUERY_STRING"]
        status = "200 OK"
        response_headers = [("Content-type", "text/plain")]
        start_response(status, response_headers)
        return [b"Hello World!\n", ("QUERY_STRING:" + params).encode("utf-8")]

    return _app


class TestDispatch(unittest.TestCase):
    def setUp(self):
        PxContext.wsgi_app = wsgi_app()

        self.headers = {
            "Host": "localhost:8000",
            "User-Agent": "Mozilla/5.0",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json",
            "Content-Length": "18",
            "Connection": "keep-alive",
        }
        self.body = b'{"key": "value"}'

    def test_dispatch_returns_response_dict(self):
        request_line = ("GET", "/hello", "HTTP/1.1")
        resp = asyncio.run(dispatch(request_line, self.headers, self.body))
        self.assertIsInstance(resp, dict)

    def test_dispatch_response_dict_has_status_headers_body(self):
        request_line = ("GET", "/hello", "HTTP/1.1")
        resp = asyncio.run(dispatch(request_line, self.headers, self.body))
        self.assertIn("status", resp)
        self.assertIn("headers", resp)
        self.assertIn("body", resp)

    def test_dispatch_response_body(self):
        request_line = ("GET", "/hello?k1=1&k2=2", "HTTP/1.1")
        resp = asyncio.run(dispatch(request_line, self.headers, self.body))
        self.assertIsInstance(resp["body"], bytes)
        self.assertEqual(resp["body"], b"Hello World!\nQUERY_STRING:k1=1&k2=2")


class TestParseRequestEnviron(unittest.TestCase):
    def setUp(self):
        self.request_line = ("POST", "/submit-form", "HTTP/1.1")
        self.headers = {
            "Host": "localhost:8000",
            "User-Agent": "Mozilla/5.0",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json",
            "Content-Length": "18",
            "Connection": "keep-alive",
        }
        self.body = b'{"key": "value"}'

    def test_parse_request_environ_returns_dict(self):
        environ = parse_request_environ(self.request_line, self.headers, self.body)
        self.assertIsInstance(environ, dict)

    def test_parse_request_environ_has_standard_keys(self):
        environ = parse_request_environ(self.request_line, self.headers, self.body)
        self.assertIn("REQUEST_METHOD", environ)
        self.assertIn("SCRIPT_NAME", environ)
        self.assertIn("PATH_INFO", environ)
        self.assertIn("QUERY_STRING", environ)
        self.assertIn("SERVER_NAME", environ)
        self.assertIn("SERVER_PORT", environ)
        self.assertIn("SERVER_PROTOCOL", environ)
        self.assertIn("CONTENT_TYPE", environ)
        self.assertIn("CONTENT_LENGTH", environ)

    def test_parse_request_environ_has_wsgi_keys(self):
        environ = parse_request_environ(self.request_line, self.headers, self.body)
        self.assertIn("wsgi.version", environ)
        self.assertIn("wsgi.url_scheme", environ)
        self.assertIn("wsgi.input", environ)
        self.assertIn("wsgi.errors", environ)
        self.assertIn("wsgi.multithread", environ)
        self.assertIn("wsgi.multiprocess", environ)
        self.assertIn("wsgi.run_once", environ)

    def test_parse_request_environ_returns_valid_environ(self):
        environ = parse_request_environ(self.request_line, self.headers, self.body)
        self.assertEqual(environ["REQUEST_METHOD"], "POST")
        self.assertEqual(environ["SCRIPT_NAME"], "")
        self.assertEqual(environ["PATH_INFO"], "/submit-form")
        self.assertEqual(environ["QUERY_STRING"], "")
        self.assertEqual(environ["SERVER_PROTOCOL"], "HTTP/1.1")
        self.assertEqual(environ["CONTENT_TYPE"], "application/json")
        self.assertEqual(environ["CONTENT_LENGTH"], "18")
        self.assertEqual(environ["HTTP_HOST"], "localhost:8000")
        self.assertEqual(environ["HTTP_USER_AGENT"], "Mozilla/5.0")
        self.assertEqual(environ["HTTP_ACCEPT_ENCODING"], "gzip, deflate")
        self.assertEqual(environ["wsgi.version"], (1, 0))
        self.assertEqual(environ["wsgi.url_scheme"], "http")
        self.assertEqual(environ["wsgi.errors"], sys.stderr)
        self.assertFalse(environ["wsgi.multithread"])
        self.assertFalse(environ["wsgi.multiprocess"])
        self.assertFalse(environ["wsgi.run_once"])

#!/usr/bin/env python3

# BoBoBo

import unittest
from unittest.mock import patch
from px.main import parse_args


class TestParseCommand(unittest.TestCase):

    def setUp(self):
        self.host = '127.0.0.1'
        self.port = 8080
        self.request_process_module = 'my_http_request_handler'
        self.wsgi_app_module = 'my_wsgi_app'

    def test_parse_args_http(self):
        with patch('sys.argv', ['px', '-H', self.host, '-P',
                                str(self.port), '--http',
                                self.request_process_module]):
            args = parse_args()
            self.assertEqual(args.host, self.host)
            self.assertEqual(args.port, self.port)
            self.assertEqual(args.request_process_module,
                             self.request_process_module)
            self.assertEqual(args.wsgi_app_module, None)

    def test_parse_args_wsgi(self):
        with patch('sys.argv', ['px', '-H', self.host, '-P', str(self.port),
                                '--wsgi', self.wsgi_app_module]):
            args = parse_args()
            self.assertEqual(args.host, self.host)
            self.assertEqual(args.port, self.port)
            self.assertEqual(args.request_process_module, None)
            self.assertEqual(args.wsgi_app_module, self.wsgi_app_module)


if __name__ == '__main__':
    unittest.main()

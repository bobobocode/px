#!/usr/bin/env python3

# BoBoBo

import unittest
from px.http import parse_http_headers, parse_http_request_line, generate_response


class TestHttpMethods(unittest.TestCase):

    def test_parse_http_request_line_valid(self):
        self.assertEqual(parse_http_request_line(b"GET /index.html HTTP/1.1"), ("GET", "/index.html", "HTTP/1.1"))
        self.assertEqual(parse_http_request_line(b"POST /login HTTP/1.0"), ("POST", "/login", "HTTP/1.0"))

    def test_parse_http_request_line_invalid(self):
        with self.assertRaises(ValueError):
            parse_http_request_line(b"GET /index.html")
        with self.assertRaises(ValueError):
            parse_http_request_line(b"GET")

    def test_parse_http_headers(self):
        headers_bytes = b"Host: www.example.com\r\nConnection: keep-alive\r\nAccept-Language: en-us,en;q=0.5\r\n\r\n"
        headers = parse_http_headers(headers_bytes)
        self.assertEqual(len(headers), 3)
        self.assertEqual(headers["Host"], "www.example.com")
        self.assertEqual(headers["Connection"], "keep-alive")
        self.assertEqual(headers["Accept-Language"], "en-us,en;q=0.5")

    def test_generate_response(self):
        response = {"status": "200 OK", "headers": {"Content-Type": "text/html"}, "body": "<h1>Hello World</h1>"}
        response_data = generate_response(response)
        self.assertEqual(response_data, b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>Hello World</h1>")


if __name__ == '__main__':
    unittest.main()

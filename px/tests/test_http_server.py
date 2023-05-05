#!/usr/bin/env python3
# BoBoBo
import unittest
from http.client import HTTPConnection

from px.http_server import start_server
from px.http_server import stop_server


class TestHttpServer(unittest.TestCase):
    async def test_hello_world(self):
        # start server with specific params
        async with start_server("localhost", 8080):
            conn = HTTPConnection("localhost", 8080)
            conn.request("GET", "/")
            response = conn.getresponse()
            self.assertEqual(response.status, 200)
            self.assertEqual(response.reason, "OK")
            self.assertEqual(response.read().decode("utf-8"), "Hello World!")

        # stop server
        await stop_server()


if __name__ == "__main__":
    unittest.main()

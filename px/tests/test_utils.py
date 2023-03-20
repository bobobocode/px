#!/usr/bin/env python3

# BoBoBo


import asyncio
import unittest
from px.utils import read_until


class TestReadUntil(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def tearDown(self):
        self.loop.close()

    async def test_read_until(self):
        reader, writer = await asyncio.open_connection('localhost', 8888, loop=self.loop)

        message = b'Hello World'
        delimiter = b' '

        # write message
        writer.write(message + delimiter)
        await writer.drain()

        # read message
        read_buffer = b''
        result, read_buffer = await read_until(read_buffer, reader, delimiter)

        self.assertEqual(result, message)
        self.assertEqual(read_buffer, b'')

        writer.close()


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3
# BoBoBo
import asyncio
from typing import Tuple


async def read_until(
    read_buffer: bytes, reader: asyncio.StreamReader, until_bytes: bytes
) -> Tuple[bytes, bytes]:
    """
    Read bytes by reader, until reach the until_bytes.
    Parameter read_buffer is used for caching bytes between multi-reads.
    """
    if not read_buffer:
        read_buffer = b""

    while True:
        end_index = read_buffer.find(until_bytes)
        if end_index != -1:
            # Found the delimiter, return the message and remaining buffer
            return (
                read_buffer[:end_index],
                read_buffer[end_index + len(until_bytes) :],
            )
        else:
            data = await reader.read(1024)
            if not data:
                return (b"", read_buffer)
            read_buffer += data

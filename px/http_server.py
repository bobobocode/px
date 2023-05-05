#!/usr/bin/env python3
# BoBoBo
import asyncio

from .http import generate_response
from .http import parse_http_headers
from .http import parse_http_request_line
from .utils import read_until


async def filter_and_send_response(resp, writer, process_module):
    """Filter response using process_module and send it to client.

    Args:
        response: The response to filter.
        writer: The StreamWriter to send the response to.
        process_module: The module containing the filter_response function.

    Returns:
        None
    """
    filtered_resp = await process_module.filter_response(resp)
    response = generate_response(filtered_resp)
    writer.write(response)
    await writer.drain()


async def handle_request(reader, writer, process_module):
    """
    Parse HTTP request bytes to request line, headers and body.
    Filter by request line and headers.
    Dispatch with http request.
    And filter response before return to client.
    """
    request_line = None
    headers = {}
    body = None

    read_buffer = b""
    while True:
        request_line_bytes, read_buffer = await read_until(read_buffer, reader, b"\r\n")
        request_line = parse_http_request_line(request_line_bytes)
        resp = await process_module.filter_request_line(request_line)
        if resp:
            await filter_and_send_response(resp, writer, process_module)
            break

        print(f"read_buffer:{read_buffer}")
        # next tow bytes
        if len(read_buffer) < 2:
            data = await reader.read(1024)
            if not data:
                writer.close()
                return
            read_buffer = read_buffer + data

        # if not just request line
        if read_buffer[:2] != b"\r\n":
            headers_bytes, read_buffer = await read_until(
                read_buffer, reader, b"\r\n\r\n"
            )
            headers = parse_http_headers(headers_bytes)
            resp = await process_module.filter_headers(headers)
            if resp:
                await filter_and_send_response(resp, writer, process_module)
                break

            content_length = headers.get("content_length", None)
            while True:
                if content_length is None:
                    body = read_buffer
                    break
                else:
                    if len(read_buffer) < content_length:
                        data = await reader.read(1024)
                        if not data:
                            writer.close()
                            return
                        read_buffer = read_buffer + data
                        continue
                    else:
                        content_length = int(content_length)
                        body = read_buffer[:content_length]

        resp = await process_module.dispatch(request_line, headers, body)
        if resp:
            await filter_and_send_response(resp, writer, process_module)
            break

    writer.close()


server = None


async def start_server(host="127.0.0.1", port=8080, process_module=None):
    global server
    server = await asyncio.start_server(
        lambda r, w: handle_request(r, w, process_module), host=host, port=port
    )

    # Keep the server running
    async with server:
        await server.serve_forever()


async def stop_server():
    global server
    if server:
        server.close()
        await server.wait_closed()

#!/usr/bin/env python3

# BoBoBo


def parse_http_request_line(request_line_bytes):
    """
    Parses the HTTP request line 

    @param request_line_bytes: bytes representation of the HTTP request line
    @return: a tuple containing the HTTP method, path, and version
    @raise ValueError: if the HTTP request line is invalid
    """
    line_str = request_line_bytes.decode('utf-8').strip()
    parts = line_str.split()

    if len(parts) != 3:
        raise ValueError("Invalid HTTP request line")
        
    method, path, version = parts
    return (method, path, version)


def parse_http_headers(headers_bytes):
    """
    Parses the HTTP headers 

    @param headers_bytes: bytes representation of the HTTP headers 
    @return: a dictionary containing the HTTP headers 
    """
    headers = {}
    lines = headers_bytes.decode().split('\r\n')
    for line in lines:
        if not line:
            continue
        key, value = line.split(': ', 1)
        headers[key] = value
    return headers


def generate_response(response):
    """
    Generates an HTTP response 

    @param response: dictionary containing response data including status, headers, and body
    @return: bytes representation of the complete HTTP response 
    """
    status_line = f'HTTP/1.1 {response["status"]}\r\n'
    header_lines = [f'{k}: {v}\r\n' for k, v in response['headers'].items()]
    headers = ''.join(header_lines)
    body = response['body'] if isinstance(response['body'], bytes) else response['body'].encode()
    response_data = f'{status_line}{headers}\r\n{body.decode()}'.encode()
    return response_data

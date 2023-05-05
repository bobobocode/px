#!/usr/bin/env python3
# BoBoBo


async def filter_request_line(request_line):
    print(f"filter request line: {request_line}")


async def filter_headers(headers):
    print(f"filter headers : {headers}")


async def dispatch(request_line, headers, body):
    print(f"dispatch {request_line} with headers and body")

    return {
        "status": "200 OK",
        "headers": {
            "Content-Type": "text/plain",
        },
        "body": "Hello, World!",
    }


async def filter_response(response):
    print(f"filter response : {response}")
    response["body"] = "Hello, World! This is Px Server!"
    return response

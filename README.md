# Px Server

Async HTTP Server in Python, and it\`s functional.
And it supports WSGI.

## Features

* High-performance asynchronous HTTP server
* Custom HTTP processor with different phrases
* Support for WSGI application

## Installation

```sh
pip install px-server
```

## Usage

To start the server, use the following command:

```
python -m px -H <host> -P <port> --http <request_process_module>
```

By default, the server listens on localhost:8080.

You can specify a custom module to handle HTTP requests with the request_process_module argument.
Here is an example of a custom HTTP request processing module:

```
async def filter_request_line(request_line):
    # process the request line
    # ...

    # return a response
    return {
        'status': '200 OK',
        'headers': {
            'Content-Type': 'text/plain',
        },
        'body': 'Hello, World!',
    }

async def filter_headers(headers):
    # process the headers
    # ...

    # return a response
    return {
        'status': '200 OK',
        'headers': {
            'Content-Type': 'text/plain',
        },
        'body': 'Hello, World!',
    }

async def dispatch(request_line, headers, body):
    # process the request
    # ...

    # return a response
    return {
        'status': '200 OK',
        'headers': {
            'Content-Type': 'text/plain',
        },
        'body': 'Hello, World!',
    }

async def filter_response(response):
    # process the response
    # ...
    response['body'] = 'Hello, World! This is filtered'

    # return a response
    return response
```

The request_process_module is a custom module that defines three functions for processing an HTTP request:
filter_request_line(), filter_headers(), filter_response and dispatch().

* The filter_request_line() function takes in the request line as a tuple parameter (method, path, version)
and returns a dictionary
that contains the HTTP response status, headers, and body. This function is responsible for filtering
and processing the request line and returning an appropriate response.

* The filter_headers() function takes in the HTTP headers as a dictionary parameter and returns a dictionary
that contains the HTTP response status, headers, and body. This function is responsible for filtering
and processing the HTTP headers and returning an appropriate response.

* The filter_response() function takes in the response that will return
to clients. Before they are returned to clients, you can custom your
response filter here.

* The dispatch() function takes in the request line, headers, and body as parameters and returns a dictionary
that contains the HTTP response status, headers, and body. This function is responsible for dispatching
the HTTP request to the appropriate handler based on the request method and URI path, processing the request,
and returning an appropriate response.

All four functions should return a dictionary with the following keys:

* status: The HTTP response status code and reason phrase, e.g. "200 OK".
* headers: A dictionary of HTTP response headers,
where the keys are the header names and the values are the header values.
* body: The HTTP response body, which can be a string or bytes object.

By defining these three functions in your request_process_module,
you can customize the processing of incoming HTTP requests to your server.

## WSGI

The Px Server supports WSGI, which can be started using the following command:

```
python -m px -H <host> -P <port> --wsgi <wsgi_app_module>
```

To use a custom WSGI app module, simply specify the module with the wsgi_app_argument. Here is an example of a simple WSGI app module:

```
def wsgi_app():
    # do some process, like building app context
    # ...

    def _app(environ, start_response):
        """Simplest wsgi app."""
        params = environ['QUERY_STRING']
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        return ['Hello World!\n'.encode('utf-8'),
                ('QUERY_STRING:' + params).encode('utf-8')]

    return _app
```

To use this module, it is important to have a function named wsgi_app within it,
which returns an WSGI app.

Notice: The parameters --http and --wsgi are mutually exclusive,
meaning only one of them can be used at a time.

## Testing

To test the server, you can use a tool like curl. For example:

```
$ curl http://localhost:8080/
Hello, World!
```

## License

This code is released under the GPL3 License. See LICENSE for more information.

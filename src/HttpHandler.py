import os
from datetime import datetime, date, time


class HttpHandler:

    def __init__(self, request, document_root):
        self.request = request
        self.document_root = document_root

    def set_general_headers(self):
        headers = 'Server: myServer\n'
        headers += 'Date: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n'
        headers += 'Connection: close\r\n'
        return headers

    def return_error_response(self, code):
        messages = {
            '403': 'Forbidden',
            '404': 'Not Found',
            '405': 'Method Not Allowed'
        }
        response = 'Http/1.1 ' + str(code) + ' ' + messages[str(code)] + '\n'
        response += self.set_general_headers()
        response += '\n\n'
        return response

    def set_content_type(self, path):
        content_types = {
            '.html': 'text/html',
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.swf': 'application/x-shockwave-flash',
        }
        file_name, file_extension = os.path.splitext(path)
        return 'Content-Type: ' + content_types[file_extension]
        # return 'Content-Type: {}'.format(content_types.get(file_extension, 'text/txt'))

    def response_to_GET(self, path):
        try:
            with open(path) as f:
                body = f.read()
        except IOError:
            return self.return_error_response(404)

        response = 'HTTP/1.1 200 OK\n'
        response += self.set_general_headers()
        response += 'Content-Length: ' + str(len(body)) + '\r\n'
        response += self.set_content_type(path)
        response += '\r\n\r\n'
        # response += '\r\nContent-Length: {}\r\n'.format(len(body))
        response += body
        return response

    def response_to_HEAD(self, path):
        try:
            with open(path) as f:
                body = f.read()
        except IOError:
            return self.return_error_response(404)

        response = 'HTTP/1.1 200 OK\n'
        response += self.set_general_headers()
        response += 'Content-Length: ' + str(len(body)) + '\r\n'
        response += self.set_content_type(path)
        return response

    def make_response(self, request, document_root):
        file_path = document_root + '/index.html'
        request_first_row = request.split(b'\r\n')[0]
        method, path, version = request_first_row.split(b' ')

        print(method)
        if method == b'GET':
            return self.response_to_GET(file_path)
        elif method == b'HEAD':
            return self.response_to_HEAD(file_path)
        else:
            return self.return_error_response(405)





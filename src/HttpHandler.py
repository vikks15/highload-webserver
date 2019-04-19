import os
from datetime import datetime
import urllib.parse

content_types = {
    '.txt': 'text/plain',
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.gif': 'image/gif',
    '.swf': 'application/x-shockwave-flash',
}

messages = {
    '403': 'Forbidden',
    '404': 'Not Found',
    '405': 'Method Not Allowed'
}

class HttpHandler:
    def __init__(self, request, document_root):
        self.request = request.decode('UTF-8')
        self.document_root = document_root

    def set_general_headers(self):
        headers = 'Server: myServer\r\n'
        headers += 'Date: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\r\n'
        headers += 'Connection: close\r\n'
        return headers

    def return_error_response(self, code):
        response = 'HTTP/1.1 ' + str(code) + ' ' + messages[str(code)] + '\n'
        response += self.set_general_headers()
        response += '\n'
        return response.encode()

    def set_content_type(self, path):
        file_name, file_extension = os.path.splitext(path)
        return 'Content-Type: ' + content_types[file_extension] + '\r\n'

    def response_to_GET(self, path):
        content_type = self.set_content_type(path)
        response = 'HTTP/1.1 200 OK\n'
        response += self.set_general_headers()
        response += content_type

        try:
            with open(path, 'rb') as f:
                body = f.read()
                size = os.stat(path).st_size
                response += 'Content-Length: ' + str(size) + '\r\n'
                response += '\n'
                final_response = response.encode()
                final_response += body

            return final_response

        except IOError:
            return self.return_error_response(404)

    def response_to_HEAD(self, path):
        if not os.path.isfile(path):
            return self.return_error_response(404)

        file_size = os.stat(path).st_size
        response = 'HTTP/1.1 200 OK\r\n'
        response += self.set_general_headers()
        response += 'Content-Length: ' + str(file_size) + '\r\n'
        response += self.set_content_type(path)
        response += '\r\n'
        return response.encode()

    def make_response(self):
        request_first_row = self.request.split('\r\n')[0].split(' ')

        if not (request_first_row[0] == 'GET' or request_first_row[0] == 'HEAD'):
            return self.return_error_response(405)  

        decoded_path = urllib.parse.unquote(request_first_row[1])  # for percent encoded urls
        path = decoded_path.split('?')[0]

        # document_root_escaping check
        if '../' in path:
            return self.return_error_response(404)

        if path[len(path)-1] == '/':
            file_path = self.document_root + path + 'index.html'
            if not os.path.isfile(file_path):
                return self.return_error_response(403)
        else:
            file_path = self.document_root + path

        if request_first_row[0] == 'HEAD':
            return self.response_to_HEAD(file_path)

        return self.response_to_GET(file_path)

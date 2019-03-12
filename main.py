import socket
from src.HttpHandler import HttpHandler
# from Queue import Queue
# import threading
# queue = Queue()

HOST, PORT = '', 8888
REQUEST_QUEUE_SIZE = 5


def handle_request(client_connection, document_root):
    request = client_connection.recv(1024)
    http_handler = HttpHandler(request, document_root)
    client_connection.sendall(bytes(http_handler.make_response(request, document_root), 'UTF-8'))

def serve_forever():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind((HOST, PORT))
    listen_socket.listen(REQUEST_QUEUE_SIZE)
    document_root = '/...way.../'
    print('Serving HTTP on port %s ...' % PORT)

    while True:
        client_connection, client_address = listen_socket.accept()
        handle_request(client_connection, document_root)
        client_connection.close()


if __name__ == '__main__':
    serve_forever()

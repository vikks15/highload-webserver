import socket
from src.HttpHandler import HttpHandler
import threading

def handle_request(listen_socket, document_root):
    while True:
        client_connection, client_address = listen_socket.accept()
        request = client_connection.recv(1024)

        if request == b'\n':
            client_connection.close()
            continue

        http_handler = HttpHandler(request, document_root)

        try:
            response = http_handler.make_response().encode()
        except:
            # images in bytes already
            response = http_handler.make_response()

        client_connection.sendall(response)
        client_connection.close()


def run_server(config):
    host = '127.0.0.1'
    port = 80
    #port = 8888
    queue_size = 5
    thread_pool = []

    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind((host, port))
    listen_socket.listen(queue_size)
    document_root = config['document_root']
    #document_root = '.'

    print('Serving HTTP on port %s ...' % port)

    for i in range(config['thread_limit']):
        current_thread = threading.Thread(target=handle_request, args=(listen_socket, document_root,))
        thread_pool.append(current_thread)
        current_thread.start()

    for thread in thread_pool:
        thread.join()


def read_config():
    config_path = '/myserver/httpd.conf'
    try:
        with open(config_path) as config_file:
            config_strings_arr = config_file.read().split('\n')
    except IOError:
        print('Cant read config')
        return

    config_data = dict()

    for line in config_strings_arr:
        key, value = line.split()[0:2]
        config_data[key] = value

    config_data['cpu_limit'] = int(config_data['cpu_limit'])
    config_data['thread_limit'] = int(config_data['thread_limit'])

    return config_data


if __name__ == '__main__':
    config = read_config()
    run_server(config)

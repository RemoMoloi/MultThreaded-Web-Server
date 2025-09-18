#!/usr/bin/env python3
import socket
import threading
import os
import time
from queue import Queue

HOST, PORT = "127.0.0.1", 8080
WWW_ROOT = "www"
LOG_FILE = "server.log"
MAX_THREADS = 10

log_lock = threading.Lock()

def log_message(message):
    with log_lock:
        with open(LOG_FILE, "a") as log_file:
            log_file.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")
        print(message)

def handle_client(client_socket, address):
    try:
        request_data = client_socket.recv(1024).decode("utf-8")
        if not request_data:
            return

        request_line = request_data.splitlines()[0]
        method, path, _ = request_line.split()
        if path == "/":
            path = "/index.html"

        file_path = os.path.join(WWW_ROOT, path.strip("/"))

        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, "rb") as f:
                response_body = f.read()
            response_line = "HTTP/1.1 200 OK\r\n"
        else:
            response_body = b"<h1>404 Not Found</h1>"
            response_line = "HTTP/1.1 404 Not Found\r\n"

        response_headers = "Server: SimplePythonServer\r\n"
        response_headers += f"Content-Length: {len(response_body)}\r\n"
        response_headers += "Connection: close\r\n"
        response_headers += "Content-Type: text/html\r\n\r\n"

        client_socket.sendall(response_line.encode() + response_headers.encode() + response_body)

        log_message(f"{address} - {method} {path} - {response_line.strip()}")
    except Exception as e:
        log_message(f"Error handling request from {address}: {e}")
    finally:
        client_socket.close()

def worker():
    while True:
        client_socket, address = connection_queue.get()
        handle_client(client_socket, address)
        connection_queue.task_done()

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        log_message(f"Server started on {HOST}:{PORT}, serving {WWW_ROOT}")

        for _ in range(MAX_THREADS):
            t = threading.Thread(target=worker, daemon=True)
            t.start()

        while True:
            client_socket, address = server_socket.accept()
            connection_queue.put((client_socket, address))

if __name__ == "__main__":
    if not os.path.exists(WWW_ROOT):
        os.makedirs(WWW_ROOT)
    connection_queue = Queue()
    run_server()

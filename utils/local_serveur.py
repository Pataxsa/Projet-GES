import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from threading import Thread

class LocalServer:
    def __init__(self, host='localhost', port=8000, directory='.'):
        self.host = host
        self.port = port
        self.directory = directory
        self.httpd = None

    def start_server(self):
        os.chdir(self.directory)
        handler = SimpleHTTPRequestHandler
        self.httpd = HTTPServer((self.host, self.port), handler)
        print(f"Server lancé à http://{self.host}:{self.port}")
        server_thread = Thread(target=self.httpd.serve_forever)
        server_thread.start()

    def stop_server(self):
        if self.httpd:
            self.httpd.shutdown()
            print("Serveur stoppé.")

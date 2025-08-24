#!/usr/bin/env python3
import http.server
import socketserver
import os
import json
from datetime import datetime

PORT = 8000
HOSTNAME = os.uname().nodename

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/info':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            info = {
                'level': 0,
                'type': 'Direct Process',
                'hostname': HOSTNAME,
                'timestamp': datetime.now().isoformat(),
                'message': 'Running directly on host OS'
            }
            self.wfile.write(json.dumps(info).encode())
        else:
            super().do_GET()

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Server running at http://localhost:{PORT}/")
    httpd.serve_forever()

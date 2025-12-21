import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8001
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def run_server():
    # Change to the directory where the script is located
    os.chdir(DIRECTORY)
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        print(f"Opening smoke test at http://localhost:{PORT}/leviv4-smoke-test.html")
        
        # Open the browser automatically
        webbrowser.open(f"http://localhost:{PORT}/leviv4-smoke-test.html")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping server...")
            httpd.shutdown()

if __name__ == "__main__":
    run_server()
